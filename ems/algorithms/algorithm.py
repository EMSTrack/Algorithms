# Framework for using algorithms and allowing for replacement
from ems.models.case import Case


# Used by the sim to select ambulances
class Algorithm:

    def select_ambulance(self,
                         ambulances: list,
                         case: Case,
                         demands: list):
        raise NotImplementedError()
