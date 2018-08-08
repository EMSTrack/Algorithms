# Selects a pre-determined ambulance for a given case
from datetime import datetime
from typing import List, Dict

from ems.algorithms.selection.ambulance_selection import AmbulanceSelectionAlgorithm
from ems.models.ambulance import Ambulance
from ems.models.case import Case


class PreDeterminedAmbulanceAlgorithm(AmbulanceSelectionAlgorithm):

    def __init__(self,
                 cases: List[Case]=None,
                 ambulances: List[Ambulance]=None):

        if cases is None:
            cases = []

        if ambulances is None:
            ambulances = []

        if len(cases) != len(ambulances):
            # TODO --- Custom exception
            raise Exception('Number of cases unequal to number of ambulances')

        # Generate dictionary of case -> ambulance mappings
        self.determined_ambulances = {}
        for case, ambulance in zip(cases, ambulances):
            self.determined_ambulances[case] = ambulance

    def register_case(self,
                      case: Case,
                      ambulance: Ambulance):
        self.determined_ambulances[case] = ambulance

    def select_ambulance(self, available_ambulances: List[Ambulance], case: Case, current_time: datetime):
        pre_det_ambulance = self.determined_ambulances[case]

        # TODO check if ambulance is available

        return pre_det_ambulance
