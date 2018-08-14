import heapq
from datetime import datetime
from typing import List

from termcolor import colored

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

    def run(self):

        case_iterator = iter(self.cases)
        pending_cases = []
        ongoing_case_states = []
        current_time = None

        # Initialize next case
        next_case = next(case_iterator)

        while len(ongoing_case_states) or next_case:

            next_ongoing_case_state_dt = ongoing_case_states[0].next_event_time if ongoing_case_states else datetime.max
            available_ambulances = [ambulance for ambulance in self.ambulances if not ambulance.deployed]

            # Process a pending case
            if pending_cases and available_ambulances:
                print(colored("Processing pending case", "yellow", attrs=["bold"]))

                case = pending_cases.pop(0)
                case_state_to_add = self.process_new_case(case, current_time)
                heapq.heappush(ongoing_case_states, case_state_to_add)

            # Look at the next case
            elif next_case and next_case.date_recorded <= next_ongoing_case_state_dt:

                print(colored("Processing next case", "yellow", attrs=["bold"]))

                current_time = next_case.date_recorded

                # Process a new case
                if available_ambulances:
                    case_state_to_add = self.process_new_case(next_case, current_time)
                    heapq.heappush(ongoing_case_states, case_state_to_add)

                # Delay a case
                else:
                    print(colored("No ambulance; Case {} added to pending cases".format(next_case.id), "red",
                                  attrs=["bold"]))
                    pending_cases.append(next_case)

                # Prepare the next case
                next_case = next(case_iterator, None)

            # Process an ongoing case event
            else:

                print(colored("Processing ongoing case", "yellow", attrs=["bold"]))

                next_ongoing_case_state = ongoing_case_states.pop(0)
                current_time = next_ongoing_case_state.next_event_time

                # Process ongoing case
                case_state_to_add = self.process_ongoing_case(next_ongoing_case_state, current_time)
                if case_state_to_add is not None:
                    heapq.heappush(ongoing_case_states, case_state_to_add)
                else:
                    self.finished_cases.append(next_ongoing_case_state.case)

            print("Busy ambulances: ", sorted([amb.id for amb in self.ambulances if amb.deployed]))
            print("Ongoing cases: ", [case_state.case.id for case_state in ongoing_case_states])
            print("Pending cases: ", [case.id for case in pending_cases])
            print(colored("Current Time: {}".format(current_time), "yellow", attrs=["bold"]))
            print("")

        return self.finished_cases, None

    # Selects an ambulance for the case and returns a Case State representing the next event to complete and the event
    # iterator
    def process_new_case(self, case: AbstractCase, current_time: datetime):

        print("Starting new case: {}".format(case.id))

        # Select an ambulance
        selected_ambulance = self.select_ambulance(case, current_time)
        selected_ambulance.deployed = True

        print("Selected ambulance: {}".format(selected_ambulance.id))

        # Add new case to ongoing cases
        case_event_iterator = iter(case)
        case_next_event = next(case_event_iterator)
        case_event_finish_datetime = current_time + self.compute_event_duration(case_next_event)

        return CaseState(case=case,
                         assigned_ambulance=selected_ambulance,
                         event_iterator=case_event_iterator,
                         next_event=case_next_event,
                         next_event_time=case_event_finish_datetime)

    # Processes the event in the case state and generates a new case state if there is another event after to process
    def process_ongoing_case(self, case_state: CaseState, current_time: datetime):

        # Perform event
        print("Finished event for case {}: {}".format(case_state.case.id,
                                                      case_state.next_event.event_type))

        new_event = next(case_state.event_iterator, None)

        # Generate new Case State pointing to the next event
        if new_event:
            new_event_finish_datetime = current_time + self.compute_event_duration(new_event)
            print("Started new event for case {}: {}".format(case_state.case.id, new_event.event_type))
            return CaseState(case=case_state.case,
                             assigned_ambulance=case_state.assigned_ambulance,
                             event_iterator=case_state.event_iterator,
                             next_event_time=new_event_finish_datetime,
                             next_event=new_event)
        # No more events
        else:
            print("Finished all events for case: {}".format(case_state.case.id))

            # Free ambulance
            case_state.assigned_ambulance.deployed = False

            # TODO -- Fix assumption that it gets back to base immediately
            case_state.assigned_ambulance.location = case_state.assigned_ambulance.base

            return None

    # Selects an ambulance for the given case
    def select_ambulance(self, case: AbstractCase, time: datetime):
        available_ambulances = [amb for amb in self.ambulances if not amb.deployed]
        selection = self.ambulance_selector.select_ambulance(available_ambulances, case, time)
        return selection

    # Checks the event type of the event, computes timestamp using algorithms, and returns timestamp
    def compute_event_duration(self, case: AbstractCase,
                               ambulance: Ambulance,
                               event: Event):

        # if event.event_type == EventType.BASE_TO_INCIDENT:
        #
        #     pass
        #
        # elif event.event_type == EventType.AT_INCIDENT:
        #
        #     pass
        #
        # elif event.event_type == EventType.INCIDENT_TO_HOSPITAL:
        #
        #     pass
        #
        # elif event.event_type == EventType.AT_HOSPITAL:
        #
        #     pass
        #
        # elif event.event_type == EventType.HOSPITAL_TO_BASE:
        #
        #     pass

        return event.duration


class CaseState:

    def __init__(self,
                 case,
                 assigned_ambulance,
                 event_iterator,
                 next_event_time,
                 next_event):
        self.case = case
        self.assigned_ambulance = assigned_ambulance
        self.next_event_time = next_event_time
        self.next_event = next_event
        self.event_iterator = event_iterator

    def __lt__(self, other):
        return self.next_event_time < other.next_event_time

# MAURICIO pseudocode
# Already decided which is next_case

# if next_case timestamp <= next_ongoing_case timestamp
#     if available_ambulances:
#         assign_ambulance
#         insert next_case into ongoing_cases
#         if len(pending_cases):
#             next_case = pending_cases.pop()
#         else:
#             next_case = next(case_iterator)
#     else:
#         insert next_case into pending_cases
#         next_case = next(case_iterator)

# PROCESS ONGOING CASES
