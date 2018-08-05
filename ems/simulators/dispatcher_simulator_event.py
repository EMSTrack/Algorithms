from copy import deepcopy
from typing import List

from ems.algorithms.selection.ambulance_selection import AmbulanceSelectionAlgorithm
from ems.models.ambulance import Ambulance
from ems.models.case import AbstractCase
from ems.simulators.simulator import Simulator


class EventBasedDispatcherSimulator(Simulator):

    def __init__(self,
                 ambulances: List[Ambulance],
                 cases: List[AbstractCase],
                 ambulance_selector: AmbulanceSelectionAlgorithm):

        super().__init__(ambulances, cases, ambulance_selector)
        self.finished_cases = []
        # self.current_time = cases[0].time if len(cases) > 0 else -1

    def run(self):

        ambulances_in_motion = []
        pending_cases = []
        working_cases = deepcopy(self.cases)
