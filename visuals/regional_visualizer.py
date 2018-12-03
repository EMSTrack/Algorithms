# ASSUMPTIONS
# (1a) The average person does NOT want to view a year's worth of simulation.
# (2a) The number of dots in total should be directly proportional to the number of seconds
# (2b) The number of dots visible should be constant to show velocity.
# (3a) There's a fixed number of ambulances

# ALLOWANCES
# (1a) I CAN enumerate every second of the simulation here.
# (2a) num_dots = num_seconds * rate of change
# (2b) It'll probably be 200 or something.
# (3a) Each ambulance can have its own color that it retains for duration of the visualization.

# The Visualizer should:
    # Know the total number of seconds of the entire simulation.
        # Make a list length num_seconds
    # Define a function to convert seconds into dots. We can set the frame rate later.
    # Make sure to know what color each ambulance is.


# Start:
    # Start time for the ambulance
    # Start and end positions, and the time it takes to reach from s to e.

# End:
    # Using the start time for the amb, calculate the number of dots to reach the end
    # Using the duration and the start time, calculate the new start time. Repeat until
    # no more paths to take.

# TODO IF AMBULANCE TRIP IS EMPTY THEN IT IS IN BASE. JUST FILL IN THE BLANKS WITH BASE_LOC


import numpy as np
import pandas as pd
from geopy import Point
from IPython import embed

from ambulance_trip import AmbulanceTrip


class RegionalVisualizer:
    """ Basically a 3d Array: time x ambulances x dot positions.
     This class is the overall visualizer that invokes reading the CSV files,
     processes them into useful data, and runs the matplotlib animations. """

    def __init__(self, source_file, ambulance_file):
        """

        :param source_file:
        :param ambulance_file:
        """

        # Read the raw data from the CSV files
        raw_data = pd.read_csv(source_file)
        amb_data = pd.read_csv(ambulance_file)

        # Get the number and starting location of the ambulances
        ambulance_bases = self.__init_ambulances(amb_data)
        self.ambulance_trips = [[] for _ in range(len(ambulance_bases))]

        self.start_time = pd.to_datetime(raw_data.iloc[[0]]['start_time'].values[0])

        # Read each row of the trips. Each row is an ambulance case.
        for index in raw_data.index:
            row = raw_data.iloc[[index]]
            amb_trip = AmbulanceTrip(row, ambulance_bases)
            self.ambulance_trips[amb_trip.ambulance_id].append(amb_trip)

        # Find the end time
        end_time = None
        for trips in self.ambulance_trips:
            if trips:
                last_trip = trips[-1]
                if not end_time or end_time < last_trip.end_time:
                    end_time = last_trip.end_time

        self.end_time = end_time
        self.num_minutes = round((self.end_time - self.start_time).seconds/60)
        embed()

    def __init_ambulances(self, data):
        """ Generates a list of colors for each ambulance, randomly. """

        ambulance_bases = [Point(
            data.iloc[[index]]['base_latitude'].values[0],
            data.iloc[[index]]['base_longitude'].values[0]
            ) for index in data.index
        ]
        return ambulance_bases

    def __str__(self):
        return "\n  ".join(['['] + [str(ambulance_trip) + ',' for ambulance_life in self.ambulance_trips \
                                    for ambulance_trip in ambulance_life ]) + "\n]"


def main():
    amb_file = '../results/ambulances.csv'
    src_file = '../results/processed_cases.csv'
    r = RegionalVisualizer(src_file, amb_file)

    print(r)
    # embed()


if __name__ == "__main__":
    print("vis starting")
    main()
    print("vis ended")