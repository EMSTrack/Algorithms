from datetime import datetime

from ems.models.ambulances.ambulance import Ambulance


class HospitalSelector:

    def select(self,
               timestamp: datetime,
               ambulance: Ambulance):
        raise NotImplementedError()
