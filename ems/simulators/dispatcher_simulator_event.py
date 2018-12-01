import heapq
from datetime import datetime

from termcolor import colored

from ems.algorithms.selection.ambulance_selection import AmbulanceSelectionAlgorithm
from ems.analysis.metrics.metric_aggregator import MetricAggregator
from ems.analysis.records.case_record import CaseRecord
from ems.analysis.records.case_record_set import CaseRecordSet
from ems.datasets.ambulance.ambulance_set import AmbulanceSet
from ems.datasets.case.case_set import CaseSet
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
                 ambulance_set: AmbulanceSet,
                 case_set: CaseSet,
                 ambulance_selector: AmbulanceSelectionAlgorithm,
                 metric_aggregator: MetricAggregator):
        super().__init__(ambulance_set, case_set, ambulance_selector, metric_aggregator)

    def run(self):

        ambulances = self.ambulance_set.ambulances
        case_record_set = CaseRecordSet()
        case_iterator = self.case_set.iterator()
        pending_cases = []
        ongoing_case_states = []
        current_time = None

        # Initialize next case
        next_case = next(case_iterator)

        while len(ongoing_case_states) or next_case:

            next_ongoing_case_state_dt = ongoing_case_states[0].next_event_time if ongoing_case_states else datetime.max
            available_ambulances = [ambulance for ambulance in ambulances if not ambulance.deployed]

            # Process a pending case
            if pending_cases and available_ambulances:

                case = pending_cases.pop(0)

                print(colored("Current Time: {}".format(current_time), "cyan", attrs=["bold"]))
                print(colored("Processing pending case: {}".format(case.id), "green"))

                case_state_to_add = self.process_new_case(ambulances, case, current_time)
                heapq.heappush(ongoing_case_states, case_state_to_add)

            # Look at the next case
            elif next_case and next_case.date_recorded <= next_ongoing_case_state_dt:

                current_time = next_case.date_recorded
                print(colored("Current Time: {}".format(current_time), "cyan", attrs=["bold"]))

                # Process a new case
                if available_ambulances:
                    print(colored("Processing new case: {}".format(next_case.id), "green", attrs=["bold"]))
                    case_state_to_add = self.process_new_case(ambulances, next_case, current_time)
                    heapq.heappush(ongoing_case_states, case_state_to_add)

                # Delay a case
                else:
                    print(colored("New case arrived but no available ambulance; Case pending".format(), "red"))
                    pending_cases.append(next_case)

                # Prepare the next case
                next_case = next(case_iterator, None)

            # Process an ongoing case event
            else:

                next_ongoing_case_state = ongoing_case_states.pop(0)
                current_time = next_ongoing_case_state.next_event_time

                print(colored("Current Time: {}".format(current_time), "cyan", attrs=["bold"]))
                print(colored("Processing ongoing case: {}".format(next_ongoing_case_state.case.id),
                              "green"))

                # Process ongoing case
                case_state_to_add, finished = self.process_ongoing_case(next_ongoing_case_state, current_time)
                if not finished:
                    heapq.heappush(ongoing_case_states, case_state_to_add)
                else:
                    case_record_set.add_case_record(next_ongoing_case_state.case_record)

            print(colored("Busy ambulances: {}".format(sorted([amb.id for amb in ambulances if amb.deployed])),
                          "yellow"))
            print(colored("Ongoing cases: {}".format([case_state.case.id for case_state in ongoing_case_states]),
                          "yellow"))
            print(colored("Pending cases: {}".format([case.id for case in pending_cases]), "red"))
            print("")
            print(colored("Metrics", "magenta", attrs=["bold"]))

            metric_kwargs = {"ambulances": ambulances,
                             "ongoing_cases": [case_state.case for case_state in ongoing_case_states],
                             "pending_cases": pending_cases}

            # Compute metrics
            metrics = self.metric_aggregator.calculate(current_time, **metric_kwargs)
            for metric_tag, value in metrics.items():
                print(colored("{}: {}".format(metric_tag, value), "magenta"))

            print("----------------------------------------------------------")

        return case_record_set, self.metric_aggregator

    # Selects an ambulance for the case and returns a Case State representing the next event to complete and the event
    # iterator
    def process_new_case(self, ambulances, case: Case, current_time: datetime):

        # Select an ambulance
        selected_ambulance = self.select_ambulance(ambulances, case, current_time)
        selected_ambulance.deployed = True

        print("Selected ambulance: {}".format(selected_ambulance.id))

        # Add new case to ongoing cases
        case_event_iterator = case.iterator(selected_ambulance, current_time)
        case_next_event = next(case_event_iterator)
        case_event_finish_datetime = current_time + case_next_event.duration

        print("Started new event (Duration {}) for case {}: {}".format(case_next_event.duration,
                                                                       case.id,
                                                                       case_next_event.event_type))

        case_record = CaseRecord(case=case,
                                 ambulance=selected_ambulance,
                                 start_time=current_time,
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
        print("Finished event: {}".format(finished_event.event_type.value))
        case_state.assigned_ambulance.location = finished_event.destination

        new_event = next(case_state.event_iterator, None)

        # Generate new Case State pointing to the next event
        if new_event:

            new_event_finish_datetime = current_time + new_event.duration
            print("Started new event: {}".format(new_event.event_type.value))
            print("Destination: {}, {}".format(new_event.destination.latitude, new_event.destination.longitude))
            print("Duration: {}".format(new_event.duration))

            # Update case state with new info
            case_state.next_event_time = new_event_finish_datetime
            case_state.next_event = new_event

            return case_state, False

        # No more events
        else:
            print(colored("Case finished", "green", attrs=["bold"]))

            # Free ambulance
            case_state.assigned_ambulance.deployed = False

            # TODO -- Fix assumption that it gets back to base immediately
            case_state.assigned_ambulance.location = case_state.assigned_ambulance.base

            return case_state, True

    # Selects an ambulance for the given case
    def select_ambulance(self, ambulances, case: Case, time: datetime):
        available_ambulances = [amb for amb in ambulances if not amb.deployed]
        selection = self.ambulance_selector.select_ambulance(available_ambulances, case, time)
        return selection
