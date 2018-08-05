import heapq
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
        self.current_time = -1

    def run(self):

        ambulances_in_motion = []

        pending_cases = []
        working_cases = deepcopy(self.cases)

        pending_events = []

        for case_index, case in enumerate(working_cases):
            for event_index, event in enumerate(case.iter()):

                event_obj = event[0]
                is_last = event[1]

                # Heap orders events by timestamp, then by case ordering, then by event ordering
                heapq.heappush(pending_events, (event_obj.origin.timestamp,
                                                case_index,
                                                event_index,
                                                event_obj,
                                                case,
                                                is_last))

        while pending_events:
            pass





            # Print current time and event after execution

