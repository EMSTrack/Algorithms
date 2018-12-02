import re
from geopy import Point
from event import Line, Dot
import pandas as pd

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