import heapq
from copy import deepcopy
from datetime import datetime
from typing import List

from ems.algorithms.selection.ambulance_selection import AmbulanceSelectionAlgorithm
from ems.models.ambulance import Ambulance
from ems.models.case import AbstractCase
from ems.models.event import Event
from ems.models.event_type import EventType
from ems.simulators.simulator import Simulator


class EventBasedDispatcherSimulator(Simulator):

    def __init__(self,
                 ambulances: List[Ambulance],
                 cases: List[AbstractCase],
                 ambulance_selector: AmbulanceSelectionAlgorithm):

        super().__init__(ambulances, cases, ambulance_selector)
        self.finished_cases = []
        self.ambulances_in_motion = []
        self.current_time = cases[0].date_recorded

    def run(self):

        pending_cases = []
        working_cases = deepcopy(self.cases)
        pending_events = []
        current_time = None

        # Case level loop
        while len(working_cases) > 0 or self.ambulances_in_motion:

            # Determine next event, pending case, and working case
            event_data = pending_events[0] if len(pending_events) > 0 else None
            working_case = working_cases[0] if len(working_cases) > 0 else None
            pending_case = pending_cases[0] if len(pending_cases) > 0 else None

            # Unpackage event data
            event_timestamp = event_data[0] if event_data is not None else datetime.max

            are_ambulances_free = not len(self.ambulances) == len(self.ambulances_in_motion)

            # Assigned values later
            next_event_case = None
            next_event_case_iter = None

            # Pending case exists and ambulances are free
            if pending_case is not None and are_ambulances_free:

                print("Starting next pending case: {}".format(pending_case.id))

                next_event_case = pending_case
                next_event_case_iter = pending_case.iterator()

                # Assign ambulance to case
                self.assign_ambulance(next_event_case)

                # Remove case from pending list
                pending_cases.pop(0)

            # Next case comes in before the next event
            elif working_case is not None and working_case.date_recorded < event_timestamp:

                # Available ambulances
                if are_ambulances_free:

                    print("Starting next working case: {}".format(working_case.id))

                    next_event_case = working_case
                    next_event_case_iter = working_case.iterator()

                    # Assign ambulance to case
                    self.assign_ambulance(next_event_case)

                # No available ambulances
                else:

                    print("Delaying next working case: {}".format(working_case.id))
                    pending_cases.append(working_case)

                # Remove case from working case list
                working_cases.pop(0)

            # Perform the next event
            elif event_data is not None:
                event = event_data[1]
                next_event_case = event_data[2]
                next_event_case_iter = event_data[3]

                # Perform event
                print("Case: {}; Finished event: {}".format(next_event_case.id, event.event_type))

                # Remove event from pending events
                pending_events.pop(0)

            else:
                raise Exception("Sim should not reach this point; no working, pending cases or pending events")

            if next_event_case_iter is not None:

                # More events, add next event of current case to pending events
                try:
                    next_event = next(next_event_case_iter)
                    event_finish_datetime = self.compute_event_finish_time(next_event)
                    heapq.heappush(pending_events, (event_finish_datetime,
                                                    next_event,
                                                    next_event_case,
                                                    next_event_case_iter))

                # No more events
                except StopIteration as e:
                    print("Finished case: {}".format(next_event_case.id))
                    self.finished_cases.append(next_event_case)

    def assign_ambulance(self, case: AbstractCase):
        pass

    # Checks the event type of the event, computes timestamp using algorithms, and returns timestamp
    def compute_event_finish_time(self,
                                  event: Event):

        event_finish_timestamp = event.destination.timestamp

        if event.event_type == EventType.BASE_TO_INCIDENT:

            pass

        elif event.event_type == EventType.AT_INCIDENT:

            pass

        elif event.event_type == EventType.INCIDENT_TO_HOSPITAL:

            pass

        elif event.event_type == EventType.AT_HOSPITAL:

            pass

        elif event.event_type == EventType.HOSPITAL_TO_BASE:

            pass

        return event_finish_timestamp

        # Add event to pending events sorted by the when the event finishes
