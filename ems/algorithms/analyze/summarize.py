# Summarize e.g. the coverage throughout the simulation

# Should use either the bytes in memory from the simulator or
# the bytes in files on the hard drive

import matplotlib.pyplot as plt

class Summarize():
    def __init__(self):
        pass

    def overall(self, coverage):
        plt.plot([x[1] for x in coverage], [x[0] for x in coverage])
        plt.ylim(0, 1)
        plt.gcf().autofmt_xdate()
        plt.show()