"""
Implementation to select the fastest ambulance.
"""

from datetime import datetime, timedelta

from ems.algorithms.hospital_selectors.hospital_selector import HospitalSelector
from ems.datasets.location.location_set import LocationSet
from ems.datasets.travel_times.travel_times import TravelTimes
from ems.models.ambulances.ambulance import Ambulance


class FastestHospitalSelector(HospitalSelector):
    """
    Implementation to select the fastest ambulance.
    """
    def __init__(self,
                 hospital_set: LocationSet,
                 travel_times: TravelTimes):
        self.hospital_set = hospital_set
        self.travel_times = travel_times

    def select(self,
               timestamp: datetime,
               ambulance: Ambulance):
        """
        Implementation to select a hospital
        """

        # Compute the closest point in set 2 to the ambulance
        loc_set_1 = self.travel_times.origins
        closest_loc_to_ambulance, _, _ = loc_set_1.closest(ambulance.location)

        # Select an ambulance to attend to the given case and obtain the its duration of travel
        chosen_hospital, _ = self.find_fastest_hospital(closest_loc_to_ambulance)

        return chosen_hospital

    def find_fastest_hospital(self, location):
        """
        Helper method to select the fastest ambulance.
        """

        shortest_time = timedelta.max
        fastest_hosp = None

        loc_set_2 = self.travel_times.destinations

        for hospital_location in self.hospital_set.locations:

            # Compute closest location in location set 2 to the hospital
            closest_loc_to_hospital = loc_set_2.closest(hospital_location)[0]

            # Compute the time from the location point mapped to the ambulance
            # to the location point mapped to the hospital
            time = self.travel_times.get_time(location, closest_loc_to_hospital)

            if shortest_time > time:
                shortest_time = time
                fastest_hosp = hospital_location

        return fastest_hosp, shortest_time
