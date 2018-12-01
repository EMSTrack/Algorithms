import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from IPython import embed

class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


class ProcessedCases:

    def __init__(self):

        self.cases = pd.read_csv('../results/processed_cases.csv')
        self.lines = []
        self.xs = []
        self.ys = []

        # Access each row and create a new list of lines

        plt.figure(1) # Just let the lines draw freely

        for index in self.cases.index:
            row = self.cases.iloc[[index]]
            x1, y1, x2, y2 = ( row.incident_longitude, row.incident_latitude,
                             row.hospital_longitude, row.hospital_latitude)

            x1 = x1.values[0]
            x2 = x2.values[0]
            y1 = y1.values[0]
            y2 = y2.values[0]

            self.lines.append(Line(x1, y1, x2, y2))

            self.xs.append(x1)
            self.xs.append(x2)
            self.ys.append(y1)
            self.ys.append(y2)

            plt.plot([x1, x2], [y1, y2])

        plt.figure(2) # Draw the lines within the boundary
        plt.xlim(-117.173017, -116.744906)
        plt.ylim(32.367460, 32.619161)
        for line in self.lines:
            plt.plot([line.x1, line.x2], [line.y1, line.y2])


        plt.figure(3) # Plot the lines freely
        plt.scatter(self.xs, self.ys)

        plt.figure(4) # Plot the points within bounds
        plt.xlim(-117.173017, -116.744906)
        plt.ylim(32.367460, 32.619161)
        plt.scatter(self.xs, self.ys)
        plt.show()



p = ProcessedCases()
# print(p.cases)

# embed()

def animate():
    """ Try to plot the lines between the emergency location
    and the hospital location """

    fig = plt.figure()

    def myfunc(i):
        print(i)

    mylist = None

    im_ani = animation.ArtistAnimation(fig, myfunc, interval=100, repeat_delay=None,
                                       blit=False)
    plt.show()
