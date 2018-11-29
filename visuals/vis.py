
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython import embed

def update_line(num, data, line):
    line.set_data(data[..., :num])
    return line,

def ani1():
    fig1 = plt.figure()

    # Fixing random state for reproducibility
    np.random.seed(19680801)

    data = np.random.rand(2, 25)
    l, = plt.plot([], [], 'r-')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.xlabel('x')
    plt.title('test')
    line_ani = animation.FuncAnimation(fig1, update_line, 25, fargs=(data, l),
                                       interval=50, blit=True)

    # To save the animation, use the command: line_ani.save('lines.mp4')
    plt.show()

def ani2():
    fig2 = plt.figure()

    x = np.arange(-19, 20)
    y = np.arange(-19, 20).reshape(-1, 1)
    base = np.hypot(x, y)
    ims = []

    for add in np.arange(20):
        ims.append((plt.pcolor(x, y, base + add, norm=plt.Normalize(0, 30)),))

    im_ani = animation.ArtistAnimation(fig2, ims, interval=50, repeat_delay=300,
                                       blit=True)

    # To save this second animation with some metadata, use the following command:
    # im_ani.save('im.mp4', metadata={'artist':'Guido'})

    plt.show()

def ani3():
    fig, ax = plt.subplots()

    x = np.arange(0, 2*np.pi, 0.01)
    line, = ax.plot(x, np.sin(x))


    def animate(i):
        line.set_ydata(np.sin(x + i/100.0))  # update the data
        return line,


    # Init only required for blitting to give a clean slate.
    def init():
        line.set_ydata(np.ma.array(x, mask=True))
        return line,

    embed()
    ani = animation.FuncAnimation(fig, animate, np.arange(1, 500), init_func=init,
                                  interval=1, blit=True)
    plt.show()

ani3()
