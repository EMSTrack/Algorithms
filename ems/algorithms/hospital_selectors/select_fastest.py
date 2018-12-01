from datetime import datetime, timedelta

from ems.algorithms.hospital_selectors.hospital_selector import HospitalSelector
from ems.datasets.location.location_set import LocationSet
from ems.datasets.travel_times.travel_times import TravelTimes
from ems.models.ambulances.ambulance import Ambulance


class FastestHospitalSelector(HospitalSelector):

    def __init__(self,
                 hospital_set: LocationSet,
                 travel_times: TravelTimes):
        self.hospital_set = hospital_set
        self.travel_times = travel_times

    def select(self,
               timestamp: datetime,
               ambulance: Ambulance):

        # Compute the closest point in set 2 to the ambulance
        loc_set_1 = self.travel_times.loc_set_1
        closest_loc_to_ambulance, _, _ = loc_set_1.closest(ambulance.location)

        # Select an ambulance to attend to the given case and obtain the its duration of travel
        chosen_hospital, travel_time = self.find_fastest_hospital(closest_loc_to_ambulance)

        return chosen_hospital

    def find_fastest_hospital(self, location):

        shortest_time = timedelta(hours=9999999)
        fastest_hosp = None

        loc_set_1 = self.travel_times.loc_set_1

        for hospital_location in self.hospital_set.locations:

            # Compute closest location in location set 2 to the hospital
            closest_loc_to_hospital = loc_set_1.closest(hospital_location)[0]

            # Compute the time from the location point mapped to the ambulance
            # to the location point mapped to the hospital
            time = self.travel_times.get_time(location, closest_loc_to_hospital)
            if shortest_time > time:
                shortest_time = time
                fastest_hosp = fastest_hosp

        return fastest_hosp, shortest_time
