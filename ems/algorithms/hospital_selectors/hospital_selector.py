"""
Abstractly defined.
"""
from datetime import datetime
from ems.models.ambulances.ambulance import Ambulance

class HospitalSelector:
    """
    Abstract design of HospitalSelector objects.
    """
    def select(self,
               timestamp: datetime,
               ambulance: Ambulance):
        """ Basic selection algorithm """
        raise NotImplementedError()
