import random
from datetime import datetime

from ems.algorithms.hospital_selectors.hospital_selector import HospitalSelector
from ems.datasets.location.location_set import LocationSet
from ems.models.ambulances.ambulance import Ambulance


class RandomHospitalSelector(HospitalSelector):

    def __init__(self, hospital_set: LocationSet):
        self.hospital_set = hospital_set

    def select(self, timestamp: datetime, ambulance: Ambulance):
        return random.choice(self.hospital_set.locations)
