import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
#import matplotlib.image as mpimg
#from PIL import Image
#forked from DEVBYSIMMI https://github.com/DevBySimmi/Gravitational-Waves-Strain, modified by morgan thomas

fig = plt.figure(figsize=(10, 10))
# ORBIT PANEL


ax1 = plt.subplot(1, 1, 1)

#ax1.imshow(res)



ax1.set_facecolor("black")
ax1.axis("off")
ax1.add_artist(ax1.patch)
ax1.patch.set_zorder(-1)

ax1.set_xlim(-12,12)
ax1.set_ylim(-12,12)


ax1.set_aspect('equal')

# Stars this is optional.

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

num_ripples = 20

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

#ripple after merge




#Animation for just the inspiral
X1=[]
Y1=[]

X2=[]
Y2=[]

frames = 500


# ANIMATION

def update(frame):

    progress = frame / frames

    radius = 6*(1-progress)

    theta = progress * 30*np.pi #changes the orbit of the blackholes and velocity

    x1 = radius*np.cos(theta)
    y1 = radius*np.sin(theta)

    x2 = -x1
    y2 = -y1

    # Black holes

    bh1.set_data([x1],[y1])
    bh2.set_data([x2],[y2])

    # Trails

    X1.append(x1)
    Y1.append(y1)

    X2.append(x2)
    Y2.append(y2)

    trail1.set_data(
        X1,
        Y1
    )

    trail2.set_data(
        X2,
        Y2
    )

    # Gravitational wave ripples

    for i, ripple in enumerate(ripples):

        r = (frame*0.08) - i*2 #effects the speed of the ripples

        if r > 0:

            x_r = r*np.cos(theta_circle)
            y_r = r*np.sin(theta_circle)

            ripple.set_data(
                x_r,
                y_r
                )

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
# saves the animation to your desktop
ani.save('growingCoil.mp4', writer = 'ffmpeg', fps = 30)
plt.show()
