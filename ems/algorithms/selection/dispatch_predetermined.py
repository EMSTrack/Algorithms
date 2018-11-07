# Selects a pre-determined ambulance for a given case
from datetime import datetime
from typing import List, Dict

from ems.algorithms.selection.ambulance_selection import AmbulanceSelectionAlgorithm
from ems.models.ambulance import Ambulance
from ems.models.cases.case import Case


class PreDeterminedAmbulanceAlgorithm(AmbulanceSelectionAlgorithm):

    def __init__(self,
                 case_ids: List[int]=None,
                 amb_units: List[str]=None):

        if case_ids is None:
            case_ids = []

        if amb_units is None:
            amb_units = []

        if len(case_ids) != len(amb_units):
            # TODO --- Custom exception
            raise Exception('Number of cases unequal to number of ambulances')

        # Generate dictionary of case -> ambulance mappings
        self.determined_ambulances = {}
        for case_id, amb_unit in zip(case_ids, amb_units):
            self.determined_ambulances[case_id] = amb_unit

    def register_case(self,
                      case_id: int,
                      amb_unit: str):
        self.determined_ambulances[case_id] = amb_unit

    def select_ambulance(self, available_ambulances: List[Ambulance], case: Case, current_time: datetime):
        pre_det_ambulance = self.determined_ambulances[case]

        # TODO --- raise exception
        if pre_det_ambulance is None:
            print("Pre determined ambulance is None")
            return None

        for ambulance in available_ambulances:
            if ambulance.unit == pre_det_ambulance:
                return ambulance

        print("Ambulance {} not listed in available ambulances".format(pre_det_ambulance))
        return None
