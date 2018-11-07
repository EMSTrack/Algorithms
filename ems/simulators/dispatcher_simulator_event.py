import heapq
from datetime import datetime
from typing import List

from termcolor import colored

from ems.algorithms.selection.ambulance_selection import AmbulanceSelectionAlgorithm
from ems.analysis.case_record import CaseRecord
from ems.datasets.case.case_set import CaseSet
from ems.models.ambulance import Ambulance
from ems.models.cases.case import Case
from ems.simulators.simulator import Simulator


# Representation of a case in progress
class CaseState:

    def __init__(self,
                 case,
                 assigned_ambulance,
                 event_iterator,
                 next_event_time,
                 next_event,
                 case_record):
        self.case = case
        self.assigned_ambulance = assigned_ambulance
        self.next_event_time = next_event_time
        self.next_event = next_event
        self.event_iterator = event_iterator
        self.case_record = case_record

    def __lt__(self, other):
        return self.next_event_time < other.next_event_time


class EventBasedDispatcherSimulator(Simulator):

    def __init__(self,
                 ambulances: List[Ambulance],
                 case_set: CaseSet,
                 ambulance_selector: AmbulanceSelectionAlgorithm):

        super().__init__(ambulances, case_set, ambulance_selector)
        self.finished_cases = []

    def run(self):

        case_iterator = self.case_set.iterator()
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
                case_state_to_add, finished = self.process_ongoing_case(next_ongoing_case_state, current_time)
                if not finished:
                    heapq.heappush(ongoing_case_states, case_state_to_add)
                else:
                    self.finished_cases.append(next_ongoing_case_state.case_record)

            print("Busy ambulances: ", sorted([amb.id for amb in self.ambulances if amb.deployed]))
            print("Ongoing cases: ", [case_state.case.id for case_state in ongoing_case_states])
            print("Pending cases: ", [case.id for case in pending_cases])
            print(colored("Current Time: {}".format(current_time), "yellow", attrs=["bold"]))
            print("")

        return self.finished_cases, None

    # Selects an ambulance for the case and returns a Case State representing the next event to complete and the event
    # iterator
    def process_new_case(self, case: Case, current_time: datetime):

        print("Starting new case: {}".format(case.id))

        # Select an ambulance
        selected_ambulance = self.select_ambulance(case, current_time)
        selected_ambulance.deployed = True

        print("Selected ambulance: {}".format(selected_ambulance.id))

        # Add new case to ongoing cases
        case_event_iterator = iter(case)
        case_next_event = next(case_event_iterator)
        case_event_finish_datetime = current_time + case_next_event.duration

        print("Started new event for case {}: {}".format(case.id, case_next_event.event_type))
        print("Event will take: {} minutes".format(case_next_event.duration))

        case_record = CaseRecord(case=case,
                                 ambulance=selected_ambulance,
                                 delay=current_time - case.date_recorded,
                                 event_history=[case_next_event])

        return CaseState(case=case,
                         assigned_ambulance=selected_ambulance,
                         event_iterator=case_event_iterator,
                         next_event=case_next_event,
                         next_event_time=case_event_finish_datetime,
                         case_record=case_record)

    # Processes the event in the case state and generates a new case state if there is another event after to process
    def process_ongoing_case(self, case_state: CaseState, current_time: datetime):

        finished_event = case_state.next_event
        case_state.case_record.event_history.append(finished_event)

        # Perform event
        print("Finished event for case {}: {}".format(case_state.case.id,
                                                      finished_event.event_type))
        case_state.assigned_ambulance.location = finished_event.destination

        new_event = next(case_state.event_iterator, None)

        # Generate new Case State pointing to the next event
        if new_event:

            new_event_finish_datetime = current_time + new_event.duration
            print("Started new event for case {}: {}".format(case_state.case.id, new_event.event_type))
            print("Event will take: {} minutes".format(new_event.duration))

            # Update case state with new info
            case_state.next_event_time = new_event_finish_datetime
            case_state.next_event = new_event

            return case_state, False

        # No more events
        else:
            print("Finished all events for case: {}".format(case_state.case.id))

            # Free ambulance
            case_state.assigned_ambulance.deployed = False

            # TODO -- Fix assumption that it gets back to base immediately
            case_state.assigned_ambulance.location = case_state.assigned_ambulance.base

            return case_state, True

    # Selects an ambulance for the given case
    def select_ambulance(self, case: Case, time: datetime):
        available_ambulances = [amb for amb in self.ambulances if not amb.deployed]
        selection = self.ambulance_selector.select_ambulance(available_ambulances, case, time)
        return selection
