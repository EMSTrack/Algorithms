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




import numpy as np
import pandas as pd

from ambulance_trip import AmbulanceTrip



class RegionalVisualizer:
    """ Basically a 3d Array: time x ambulances x dot positions """

    def __init_ambulances(self, count):
        """ Generates a list of colors for each ambulance, randomly. """
        self.ambulance_colors = []
        for i in range(0, count):
            self.ambulance_colors.append(None)

    def __init__(self, source_file):
        """
        Get the starting location for each path
        Get the number of ambulances
        Read in the cases, convert them into paths
        Put each path into the list.

        :param source_file:
        """

        raw_data = pd.read_csv(source_file)

        np.array([[[]]])

        self.ambulance_trips = []

        for index in raw_data.index:
            row = raw_data.iloc[[index]]
            a = AmbulanceTrip(row)
            self.ambulance_trips.append(a)

    def __str__(self):
        return str(self.ambulance_trips)



def main():

    srcfile = '../results/processed_cases.csv'
    r = RegionalVisualizer(srcfile)

    for a in r.ambulance_trips:
        print(a)


if __name__ == "__main__":
    print("main starting")
    main()
    print("main ended")