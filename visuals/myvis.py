import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import pandas as pd
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

        # Access each row and create a new list of lines
        for index in self.cases.index:
            row = self.cases.iloc[[index]]
            x1, y1, x2, y2 = (row.incident_latitude, row.incident_longitude,
                            row.hospital_latitude, row.hospital_longitude)

            x1 = x1.values[0]
            x2 = x2.values[0]
            y1 = y1.values[0]
            y2 = y2.values[0]

            self.lines.append(Line(x1, y1, x2, y2))
            plt.plot([x1, x2], [y1, y2])
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
