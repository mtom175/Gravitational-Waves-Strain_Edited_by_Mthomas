import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.signal import chirp

# ============================================================
# PARAMETERS
# ============================================================

duration = 10.0
sample_rate = 4000

t = np.linspace(
    0,
    duration,
    int(duration * sample_rate)
)

# ============================================================
# GRAVITATIONAL WAVE SIGNAL
# ============================================================

wave = chirp(
    t,
    f0=20,
    f1=500,
    t1=duration,
    method='quadratic'
)

amp = (t / duration) ** 2

signal = amp * wave

ring_start = int(0.85 * len(t))

ring_t = np.linspace(
    0,
    duration * 0.15,
    len(t) - ring_start
)

signal[ring_start:] = (
    np.exp(-25 * ring_t)
    * np.sin(2 * np.pi * 180 * ring_t)
)

noise = np.random.normal(
    0,
    0.05,
    len(signal)
)

strain = signal + noise

# ============================================================
# FFT
# ============================================================

fft_vals = np.fft.fft(strain)

freqs = np.fft.fftfreq(
    len(strain),
    1 / sample_rate
)

positive = freqs > 0

# ============================================================
# FIGURE
# ============================================================

fig = plt.figure(figsize=(16, 10))

# ============================================================
# ORBIT PANEL
# ============================================================

ax1 = plt.subplot2grid((2,2),(0,0))

ax1.set_facecolor("black")

ax1.set_title(
    "Binary Black Hole Merger",
    color="white"
)

ax1.set_xlim(-12,12)
ax1.set_ylim(-12,12)

ax1.set_aspect('equal')

# Starfield

np.random.seed(42)

stars_x = np.random.uniform(-12,12,300)
stars_y = np.random.uniform(-12,12,300)

ax1.scatter(
    stars_x,
    stars_y,
    s=2,
    color='white'
)

# Black holes

bh1, = ax1.plot(
    [],
    [],
    'ko',
    markersize=18
)

bh2, = ax1.plot(
    [],
    [],
    'ko',
    markersize=18
)

# Accretion disks

disk1, = ax1.plot(
    [],
    [],
    color='orange',
    lw=4,
    alpha=0.7
)

disk2, = ax1.plot(
    [],
    [],
    color='orange',
    lw=4,
    alpha=0.7
)

# Trails

trail1, = ax1.plot(
    [],
    [],
    'cyan',
    lw=1
)

trail2, = ax1.plot(
    [],
    [],
    'magenta',
    lw=1
)

# Ripple waves

num_ripples = 10

ripples = []

for _ in range(num_ripples):

    ripple, = ax1.plot(
        [],
        [],
        color='white',
        lw=1,
        alpha=0.6
    )

    ripples.append(ripple)

theta_circle = np.linspace(
    0,
    2*np.pi,
    300
)

# ============================================================
# STRAIN PANEL
# ============================================================

ax2 = plt.subplot2grid((2,2),(0,1))

ax2.set_title(
    "Gravitational Wave Strain"
)

ax2.set_xlim(0,duration)

ax2.set_ylim(
    np.min(strain)*1.2,
    np.max(strain)*1.2
)

ax2.grid()

line, = ax2.plot(
    [],
    [],
    lw=1
)

# ============================================================
# FFT PANEL
# ============================================================

ax3 = plt.subplot2grid(
    (2,2),
    (1,0),
    colspan=2
)

ax3.plot(
    freqs[positive],
    np.abs(fft_vals[positive])
)

ax3.set_xlim(0,600)

ax3.set_title(
    "Frequency Spectrum (FFT)"
)

ax3.set_xlabel(
    "Frequency (Hz)"
)

ax3.set_ylabel(
    "Amplitude"
)

ax3.grid()

# ============================================================
# HISTORY
# ============================================================

x1_hist=[]
y1_hist=[]

x2_hist=[]
y2_hist=[]

frames = 700

# ============================================================
# ANIMATION
# ============================================================

def update(frame):

    progress = frame / frames

    radius = 4*(1-progress)+0.15

    theta = progress * 30*np.pi

    x1 = radius*np.cos(theta)
    y1 = radius*np.sin(theta)

    x2 = -x1
    y2 = -y1

    # Black holes

    bh1.set_data([x1],[y1])
    bh2.set_data([x2],[y2])

    # Accretion disks

    disk_r = 0.8

    disk1.set_data(
        x1 + disk_r*np.cos(theta_circle),
        y1 + disk_r*np.sin(theta_circle)
    )

    disk2.set_data(
        x2 + disk_r*np.cos(theta_circle),
        y2 + disk_r*np.sin(theta_circle)
    )

    # Trails

    x1_hist.append(x1)
    y1_hist.append(y1)

    x2_hist.append(x2)
    y2_hist.append(y2)

    trail1.set_data(
        x1_hist,
        y1_hist
    )

    trail2.set_data(
        x2_hist,
        y2_hist
    )

    # Gravitational wave ripples

    for i, ripple in enumerate(ripples):

        r = (frame*0.08) - i*1.5

        if r > 0:

            x_r = r*np.cos(theta_circle)
            y_r = r*np.sin(theta_circle)

            ripple.set_data(
                x_r,
                y_r
            )

            ripple.set_alpha(
                max(
                    0,
                    1-r/12
                )
            )

        else:

            ripple.set_data([],[])

    # Strain graph

    idx = int(
        progress * len(t)
    )

    line.set_data(
        t[:idx],
        strain[:idx]
    )

    return (
        bh1,
        bh2,
        disk1,
        disk2,
        trail1,
        trail2,
        line,
        *ripples
    )

ani = FuncAnimation(
    fig,
    update,
    frames=frames,
    interval=20,
    blit=True
)

plt.tight_layout()
plt.show()