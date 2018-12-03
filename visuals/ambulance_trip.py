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

    def __init__(self, row, ambulances):
        """ A single trip of an ambulance has any number of lines.
        Alternates between stationary and traveling. """

        self.row = {k: row[k].values[0] for k in row} # TODO Don't save this in the object
        self.ambulances = ambulances # TODO also dont keep this in the object

        # cast the appropriate types
        self.__location()
        self.__duration()
        self._dots_and_lines() # TODO Make clear what is being saved to self

    def __location(self):
        """ Using regexs to convert lat, lons from doubles into geopy.Points """

        # Match all non-BASE location points.
        names = set()
        for k in self.row:
            if any([
                re.match("[A-Z]*[a-z]*_latitude", k),
                re.match("[A-Z]*[a-z]*_longitude", k)]
            ):
                names.add(k.split("_")[0])

        # Recreate them as geopy.Points
        for location_name in names:
            lat = self.row[location_name + "_latitude"]
            lon = self.row[location_name + "_longitude"]
            self.row[location_name + "_point"] = Point(lat, lon) # TODO Don't save this in self.
            del self.row[location_name + "_latitude"]
            del self.row[location_name + "_longitude"]

    def __duration(self):
        """ For each ___duration, convert into timedelta.  """

        self.row['start_time'] = pd.to_datetime(self.row['start_time']) # TODO Don't save this in self.

        for k in self.row:
            if "_duration" in k:
                self.row[k] = pd.to_timedelta(self.row[k])

    def _dots_and_lines(self):
        """
        Converts the ambulance trip into dots and lines.

        :param l: list of list of strings denoting stationary or travel actions
        :return:
        """

        self.ambulance_id = self.row['ambulance']
        events = []

        # Travel from base to incident
        l1 = Line(
            self.ambulances[self.ambulance_id],
            self.row["incident_point"],
            self.row['start_time'],
            self.row["TO_INCIDENT_duration"]
        )
        events.append(l1)

        # Stationary time at incident
        d1 = Dot(
            self.row['incident_point'],
            events[-1].end_time(),
            self.row['AT_INCIDENT_duration']
        )
        events.append(d1)

        # From incident to hospital
        l2 = Line(
            self.row['incident_point'],
            self.row['hospital_point'],
            events[-1].end_time(),
            self.row['TO_HOSPITAL_duration'])
        events.append(l2)

        # Time at hospital
        d2 = Dot(
            self.row['hospital_point'],
            events[-1].end_time(),
            self.row['AT_INCIDENT_duration']
        )
        events.append(d2)

        # From hospital to base
        l3 = Line(
            self.row['hospital_point'],
            self.ambulances[self.ambulance_id],
            events[-1].end_time(),
            self.row['TO_BASE_duration']
        )
        events.append(l3)

        self.events = events # TODO DO SAVE THIS IN SELF. Just od it up there.
        self.end_time = events[-1].end_time() + self.row['TO_BASE_duration'] # TODO same with this one

        # Time at base should be calculate from this endtime and next start_time

    def __str__(self):
        print("\n    ".join([str(event) for event in self.events]) + "\n" + str(self.end_time))
        return "\n\n    ".join([str(event) for event in self.events]) + "\n" + \
               "end: " + str(self.end_time) + "\n"

    def get_end_time(self):
        return self.end_time