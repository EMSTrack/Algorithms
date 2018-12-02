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
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import re
from geopy import Point


class Event:

    def __init__(self):
        pass

    def end_time(self):
        raise NotImplementedError


class Dot(Event):
    """ Represents the location of the ambulance over time."""
    def __init__(self, location, starting_time, duration):
        """

        :param location:
        :param starting_time:
        :param duration:
        """
        pass


class Line(Event):
    """ Represents the edge of the ambulance over time. """
    def __duration_as_dots(self):
        """
        Longer distance shown by distance of the line.
        Longer time shown by the number of dots that get drawn before it finishes.
        """

        return None

    def __init__(self, starting_point, ending_point, starting_time, duration):
        """ Defines the points between the starting point and ending point. """
        pass


class AmbulanceTrip:
    """ Each case should have three instances of these enumerated.
    Takes the data from the CSV and changes into start dot, end dot, and
    range of dots that is going to be displayed at each second of the simulation.

    The number of dots won't work anymore.

    Let's say one dot per minute?
    """

    def __location(self):
        """Convert lat, lons from doubles into geopy.Points"""

        names = set()
        for k in self.row:
            if any([
                re.match("[A-Z]*[a-z]*_latitude", k),
                re.match("[A-Z]*[a-z]*_longitude", k)]
            ):
                names.add(k.split("_")[0])

        for location_name in names:
            lat = self.row[location_name + "_latitude"]
            lon = self.row[location_name + "_longitude"]
            self.row[location_name + "_point"] = Point(lat, lon)
            del self.row[location_name + "_latitude"]
            del self.row[location_name + "_longitude"]

    def __duration(self):
        """ For each ___duration, convert into timedelta.  """

        self.row['start_time'] = pd.to_datetime(self.row['start_time'])

        for k in self.row:
            if "_duration" in k:
                self.row[k] = pd.to_timedelta(self.row[k])

    def __init__(self, row):
        """
        A single trip of an ambulance has any number of lines.
        Alternates between stationary and traveling.
        :param amb_id:
        :param starts:
        :param ends:
        :param durations:
        """

        self.row = {k: row[k].values[0] for k in row}

        # cast the appropriate types
        self.__location()
        self.__duration()

    def __str__(self):
        return str(self.row)

    def dots_and_lines(self):
        """
        TODO Converts the ambulance trip into dots and lines.
        :param l: list of list of strings denoting stationary or travel actions
        :return:
        """

        events = []

        # From base to incident
        Line()

        # Time at incident
        Dot(
            self.row['incident_point'],
            self.row["start_time"] + self.row['TO_INCIDENT_duration'],
            self.row['AT_INCIDENT_duration']
        )

        # From incident to hospital
        Line(
            self.row['incident_point'],
            self.row['hospital_point'],
            self.row["start_time"] + self.row['TO_INCIDENT_duration'] + self.row['AT_INCIDENT_duration'],
            self.row['TO_HOSPITAL_duration'])

        # Time at hospital

        # From hospital to base

        # Time at base
    def end_time(self):
        raise NotImplementedError

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