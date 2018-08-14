import heapq
from copy import deepcopy
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
        self.current_time = cases[0].date_recorded

    def run(self):

        case_iterator = iter(self.cases)

        ongoing_cases = []
        pending_cases = []

        current_time = None

        next_case = next(case_iterator)

        while len(ongoing_cases) and next_case:

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
            pass

    def run(self):

        unstarted_cases = deepcopy(self.cases)
        ambulances_in_motion = []
        ongoing_cases = []
        pending_cases = []
        pending_events = []
        selected_ambulances = {}
        current_time = None

        # Case level loop
        while len(unstarted_cases) > 0 or ambulances_in_motion:

            # Determine next event, pending case, and case
            event_data = pending_events[0] if len(pending_events) > 0 else None
            unstarted_case = unstarted_cases[0] if len(unstarted_cases) > 0 else None
            pending_case = pending_cases[0] if len(pending_cases) > 0 else None

            # Unpackage event data
            event_timestamp = event_data[0] if event_data is not None else datetime.max

            # Compute ambulances currently in motion
            ambulances_in_motion = [amb for amb in self.ambulances if amb.deployed]
            are_ambulances_free = not len(self.ambulances) == len(ambulances_in_motion)

            # Assigned values later
            next_event_case = None
            next_event_case_iter = None

            # Pending case exists and ambulances are free
            if pending_case is not None and are_ambulances_free:

                next_event_case = pending_case
                next_event_case_iter = pending_case.iterator()

                # Assign ambulance to case
                amb = self.select_ambulance(next_event_case, current_time)
                amb.deployed = True
                selected_ambulances[next_event_case.id] = amb

                # Remove case from pending list
                pending_cases.pop(0)

                # Add case to ongoing
                ongoing_cases.append(pending_case)

                print("Assigning ambulance {} to pending case: {}".format(amb.id, pending_case.id))

            # Next case comes in before the next event
            elif unstarted_case is not None and unstarted_case.date_recorded < event_timestamp:

                current_time = unstarted_case.date_recorded

                # Available ambulances
                if are_ambulances_free:

                    next_event_case = unstarted_case
                    next_event_case_iter = unstarted_case.iterator()

                    # Assign ambulance to case
                    amb = self.select_ambulance(next_event_case, current_time)
                    amb.deployed = True
                    selected_ambulances[next_event_case.id] = amb

                    # Add case to ongoing
                    ongoing_cases.append(unstarted_case)

                    print("Assigning ambulance {} to next case: {}".format(amb.id, unstarted_case.id))

                # No available ambulances
                else:

                    print(colored("Delaying next unstarted case: {}".format(unstarted_case.id), "red", attrs=["bold"]))
                    pending_cases.append(unstarted_case)

                # Remove case from unstarted case list
                unstarted_cases.pop(0)

            # Perform the next event
            elif event_data is not None:

                current_time = event_timestamp

                # Unpackage event data
                event = event_data[2]
                next_event_case = event_data[3]
                next_event_case_iter = event_data[4]

                # Perform event
                print("Finished event for case {}: {}".format(next_event_case.id, event.event_type))

                # Remove event from pending events
                pending_events.pop(0)

            else:
                raise Exception("Sim should not reach this point; no unstarted, pending cases or pending events")

            if next_event_case_iter is not None:

                # More events, add next event of current case to pending events
                try:
                    next_event = next(next_event_case_iter)
                    event_finish_datetime = self.compute_event_finish_time(next_event)
                    heapq.heappush(pending_events, (event_finish_datetime,
                                                    next_event_case.id,
                                                    next_event,
                                                    next_event_case,
                                                    next_event_case_iter))
                    duration = event_finish_datetime - current_time
                    print("Case {}; Begin {}; Duration: {}".format(next_event_case.id, next_event.event_type, duration))

                # No more events
                except StopIteration as e:
                    print("Finished case: {}".format(next_event_case.id))
                    self.finished_cases.append(next_event_case)

                    # Remove case from ongoing cases
                    ongoing_cases = [case for case in ongoing_cases if not case.id == next_event_case.id]

                    # Free ambulance
                    selected_ambulances[next_event_case.id].deployed = False

            print("Busy ambulances: ", sorted([amb.id for amb in ambulances_in_motion]))
            print("Ongoing cases: ", [case.id for case in ongoing_cases])
            print("Pending cases: ", [case.id for case in pending_cases])
            print(colored("Current Time: {}".format(current_time), "yellow", attrs=["bold"]))
            print("")

        return self.finished_cases, None

    # Selects an ambulance for the given case
    def select_ambulance(self, case: AbstractCase, time: datetime):
        available_ambulances = [amb for amb in self.ambulances if not amb.deployed]
        selection = self.ambulance_selector.select_ambulance(available_ambulances, case, time)
        return selection

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
