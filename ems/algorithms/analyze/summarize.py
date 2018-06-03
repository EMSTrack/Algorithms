# Summarize e.g. the coverage throughout the simulation

# Should use either the bytes in memory from the simulator or
# the bytes in files on the hard drive

import matplotlib.pyplot as plt

class Summarize():
    """

    """
    def __init__(self):
        """

        """
        # TODO maybe the coverage data are instance variables instead?
        pass

    def overall(self, coverage):
        """

        :param coverage:
        :return:
        """

        plt.plot(
            [x[1] for x in coverage],
            [x[0] for x in coverage],
        )

        plt.ylim(0, 1)
        plt.gcf().autofmt_xdate()

        plt.xlabel('datetime')
        plt.ylabel('coverage in percent')

        plt.show()

    def specific(self, points, demands):
        """
        :param points:
        :param demands:
        :return:
        """
        selected = points[0][2] # TODO is wrong argument assumption

        demand_points = list(zip(selected, demands.locations))

        xs = [x[1].longitude for x in demand_points if x[0] > 0]
        ys = [x[1].latitude for x in demand_points if x[0] > 0]

        plt.scatter(xs, ys,
                    color='green',
                    label='covered'

        )

        xs = [x[1].longitude for x in demand_points if x[0] == 0]
        ys = [x[1].latitude for x in demand_points if x[0] == 0]

        plt.scatter(xs, ys,
                    color='red',
                    label='uncovered'
                    )

        plt.xlabel('Longitude')
        plt.ylabel('Latitude')

        plt.legend()

        plt.show()

    def duration(self, durations):
        # For each case plot the duration
        plt.plot([d.total_seconds()/60.0 for d in durations])
        plt.show()
