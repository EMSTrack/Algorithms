import heapq
from copy import deepcopy
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

        # Case level loop
        while len(working_cases) > 0:

            # Determine next event, pending case, and working case
            event_data = pending_events[0] if len(pending_events) > 0 else None
            working_case = working_cases[0] if len(working_cases) > 0 else None
            pending_case = pending_cases[0] if len(pending_cases) > 0 else None

            # Unpackage event data
            event_timestamp = event_data[0]
            event = event_data[1]
            event_case = event_data[2]

            are_ambulances_free = not len(self.ambulances) == len(self.ambulances_in_motion)

            # Pending case exists and there are now ambulances free
            if pending_case is not None and are_ambulances_free:

                # Add first event of pending case to the pending events
                first_event = next(pending_case.iter())
                self.add_event(pending_events=pending_events,
                               event=first_event,
                               case=pending_case)

                # Remove case from pending list
                pending_cases.pop(0)

            # Next case comes in before the next event
            elif working_case is not None and working_case.date_recorded < event_timestamp:

                # Available ambulances
                if are_ambulances_free:

                    # Deploy next working case
                    first_event = next(working_case.iter())
                    self.add_event(pending_events=pending_events,
                                   event=first_event,
                                   case=working_case)

                # No available ambulances
                else:
                    pending_cases.append(working_case)

                # Remove case from working case list
                working_cases.pop(0)

            # Perform the next event
            else:
                print("Case: {}; {}".format(event_case.id, event.event_type))
                try:
                    next_event = next(event_case.iter())
                    self.add_event(pending_events=pending_events,
                                   event=next_event,
                                   case=working_case)
                except Exception as e:
                    print("Last event for case {} finished".format(event_case.id))
                    self.finished_cases.append(event_case)

    # Checks the event type of the event and computes values via algorithms (e.g. ambulance selection, travel times)
    # Then adds the event to a pending list of events
    def add_event(self,
                  pending_events: List[Event],
                  event: Event,
                  case: AbstractCase):

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

        # Add event to pending events sorted by the when the event finishes
        heapq.heappush(pending_events, (event_finish_timestamp,
                                        event,
                                        case))
