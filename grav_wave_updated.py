import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.signal import chirp
#BY DEVBYSIMMI https://github.com/DevBySimmi/Gravitational-Waves-Strain
# ============================================================
# PARAMETERS
# ============================================================




# ============================================================
# FIGURE
# ============================================================

fig = plt.figure(figsize=(10, 10))
fig.suptitle('Gravitional wave inspiral')
# ============================================================
# ORBIT PANEL
# ============================================================

ax1 = plt.subplot2grid((1,1),(0,0))

ax1.set_facecolor("black")



ax1.set_xlim(-12,12)
ax1.set_ylim(-12,12)


ax1.set_aspect('equal')

# Starfield

np.random.seed(84)

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
    'o',
    color = 'white',
    markersize=30

)

bh2, = ax1.plot(
    [],
    [],
    'o',
    color = 'orange',
    markersize=30
)

# Accretion disks

#disk1, = ax1.plot(
#    [],
#    [],
#    color='white'
#)

#disk2, = ax1.plot(
#    [],
#    [],
#    color='orange'
#)

# Trails

trail1, = ax1.plot(
    [],
    [],
    'white',
    lw=1
)

trail2, = ax1.plot(
    [],
    [],
    'orange',
    lw=1
)

# Ripple waves

num_ripples = 12

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
#Animation for just the inspiral
x1_hist=[]
y1_hist=[]

x2_hist=[]
y2_hist=[]

frames = 500

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

    #disk_r = 0.8

    #disk1.set_data(
    #    x1 + disk_r*np.cos(theta_circle),
    #    y1 + disk_r*np.sin(theta_circle)
    #)

    #disk2.set_data(
    #    x2 + disk_r*np.cos(theta_circle),
    #    y2 + disk_r*np.sin(theta_circle)
    #)

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

    return (
        bh1,
        bh2,
        trail1,
        trail2,
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
# saves the animation in our desktop
ani.save('growingCoil.mp4', writer = 'ffmpeg', fps = 30)
plt.show()
