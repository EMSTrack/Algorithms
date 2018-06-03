# Summarize e.g. the coverage throughout the simulation

# Should use either the bytes in memory from the simulator or
# the bytes in files on the hard drive

import matplotlib.pyplot as plt
import numpy as np
from datetime import timedelta
from statistics import mean

class Summarize():
    """

    """
    def __init__(self,
                 num_cases,
                 num_days,
                 num_ambulances
                 ):
        """

        """
        # TODO maybe the coverage data are instance variables instead?
        self.num_cases = num_cases
        self.num_days = num_days
        self.num_ambulances = num_ambulances


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

        plt.title('Number of cases {} days {} ambulances {}\n'
                  'Average Coverage: {}%'.format(
            self.num_cases, self.num_days, self.num_ambulances,
            mean([x[0] for x in coverage])*100
        ))

        plt.show()

    def specific(self, points, demands):
        """
        :param points:
        :param demands:
        :return:
        """

        # Chooses the minimum coverage during summary,finds its index

        percentages = [point[0] for point in points]
        ind = np.argmin(percentages)


        selected = points[ind][2] # TODO is wrong argument assumption

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

        plt.title('Number of cases {} days {} ambulances {}. \n'
                  'Datetime: {}\n'
                  'Coverage: {}%'.format(
            self.num_cases, self.num_days, self.num_ambulances,
            points[ind][1], points[ind][0]*100
        ))


        plt.gcf().autofmt_xdate()
        plt.legend()

        plt.show()

    def duration(self, start_times, durations):
        # For each case plot the duration
        dur = [d.total_seconds() / 60.0 for d in durations]

        plt.scatter(start_times,
                    dur,
                    color='red'
                    )
        plt.xlim(start_times[0] - timedelta(days=0.2),
                 start_times[-1] + timedelta(days=0.2)
                 )
        plt.gcf().autofmt_xdate()

        plt.title('Number of cases {} days {} ambulances {}\n'
                  'Average Duration: {} minutes'.format(
            self.num_cases, self.num_days, self.num_ambulances,
            mean(dur)
        ))

        plt.ylim(20, 100)
        plt.ylabel('Case Duration in Minutes')

        plt.show()
