# Runs the simulation.

import datetime
from copy import deepcopy
from typing import List

from termcolor import colored

from ems.algorithms.selection.ambulance_selection import AmbulanceSelectionAlgorithm
from ems.algorithms.analysis.demand_coverage import DemandCoverage
from ems.models.ambulance import Ambulance
from ems.models.case import Case
from ems.simulators.simulator import Simulator


class DispatcherSimulator(Simulator):

    def __init__(self,
                 ambulances: List[Ambulance],
                 cases: List[Case],
                 ambulance_selector: AmbulanceSelectionAlgorithm,
                 coverage_alg: DemandCoverage):

        self.finished_cases = []
        self.current_time = cases[0].datetime if len(cases) > 0 else -1
        self.demand_coverage = coverage_alg
        super(DispatcherSimulator, self).__init__(ambulances, cases, ambulance_selector)

    def run(self):

        ambulances_in_motion = []
        pending_cases = []
        working_cases = deepcopy(self.cases)
        event = Event.START_CASE

        # Iterate while there are ambulances moving or cases to dispatch
        while working_cases or ambulances_in_motion:

            print()
            print(colored("Current Time: {}".format(self.current_time), "yellow", attrs=["bold"]))
            print(colored("Current Event: {}".format(event), "yellow", attrs=["bold"]))

            # Stage 1: Perform event for this time step
            if event == Event.RETIRE_AMBULANCE:

                # Retire ambulance
                ambulances_in_motion = self.finish_ambulances(ambulances_in_motion, self.current_time)

            elif event == Event.DELAY_CASE:

                # Get next working case and add it to pending cases
                case = working_cases.pop(0)
                pending_cases.append(case)

                print(colored("No available ambulances to deal with incoming case: {} at {}".format(case.id,
                                                                                                    case.datetime),
                              "red"))

            elif event == Event.START_CASE:

                # Get next pending case if there are any and start it
                # If no pending cases exist, start the next working case
                case = pending_cases.pop(0) if len(pending_cases) > 0 else working_cases.pop(0)
                self.start_case(case, ambulances_in_motion, self.current_time)

            else:
                # Should never reach this point
                print("Invalid Event")

            # Stage 2: Determine the next event
            # Event Delay Case:         If no ambulances are available and next case occurs before any ambulance gets
            #                           back
            # Event Retire Ambulance:   If ambulances are currently handling cases and the ambulance gets back before
            #                           next case occurs
            # Event Start Case:         If ambulances are available and next case occurs before any ambulance gets back
            #
            # Finish when no more cases and no more ambulances attending cases

            # Loop end condition - No more case or moving ambulances
            if not pending_cases and not working_cases and not ambulances_in_motion:
                # TODO The analysis calls need to be to the Coverage instance
                # total_cov = sum(self.measured_coverage)
                # avg_cov = total_cov/len(self.measured_coverage)
                # print("Average analysis: ", avg_cov)
                avg = self.demand_coverage.avg_coverage()
                min = self.demand_coverage.min_coverage()
                max = self.demand_coverage.max_coverage()
                stddev = self.demand_coverage.std_dev_coverage()
                print("Average, Min, Max, Std Dev of Coverages: ", avg, min, max, stddev)
                return self.finished_cases

            # Sort all ambulances by end times
            ambulances_in_motion = sorted(ambulances_in_motion, key=lambda k: k.end_time)

            # Boolean to determine if any ambulances are available to deploy
            ambulances_available = False if len(self.ambulances) == len(ambulances_in_motion) else True

            # If there are any cases that still have not been started
            if pending_cases or working_cases:

                # If there are no ambulances attending to a case, start the next case
                if not ambulances_in_motion:

                    # If any pending cases, start those, otherwise get the next working case
                    next_case = pending_cases[0] if pending_cases else working_cases[0]
                    event = Event.START_CASE
                    self.current_time = self.current_time if pending_cases else next_case.datetime

                # Ambulances are currently attending to cases
                else:

                    # Get the next time an ambulance will be available
                    next_available_amb = ambulances_in_motion[0]
                    ambulance_release_time = next_available_amb.end_time

                    # No available ambulances (we will either delay the next case or release an ambulance)
                    if not ambulances_available:

                        # Since we will only be delaying (not starting) we only care about the next working case
                        next_case = working_cases[0]
                        next_case_time = next_case.datetime

                        # Delay next case if it will arrive before any ambulance will finish
                        if ambulance_release_time > next_case_time:

                            event = Event.DELAY_CASE
                            self.current_time = next_case_time

                        # If ambulance returns first, set the event to retire that ambulance
                        else:

                            event = Event.RETIRE_AMBULANCE
                            self.current_time = ambulance_release_time

                    # Ambulances are available for dispatch (either start case or release an ambulance)
                    else:

                        # Since we may be starting a case, we want to get the earliest case in pending if pending
                        # cases exist
                        next_case = pending_cases[0] if pending_cases else working_cases[0]
                        next_case_time = next_case.datetime

                        # Start the next case if it will arrive or has already arrived (pending)
                        # before any ambulance will finish
                        if ambulance_release_time > next_case_time:

                            event = Event.START_CASE
                            self.current_time = next_case_time

                            # If ambulance returns first, set the event to retire that ambulance
                        else:

                            event = Event.RETIRE_AMBULANCE
                            self.current_time = ambulance_release_time

            # No cases left; retire the next ambulance that is in service
            else:
                # Get the next time an ambulance will be available
                next_available_amb = ambulances_in_motion[0]
                ambulance_release_time = next_available_amb.end_time

                # No cases left: must retire any remaining ambulances
                event = Event.RETIRE_AMBULANCE
                self.current_time = ambulance_release_time

            print("Busy ambulances: ", sorted([amb.id for amb in ambulances_in_motion]))
            print("Pending cases: ", [case.id for case in pending_cases])

        # TODO return "results" object with more potential information
        # Compute average analysis:
        # total_cov = sum(self.measured_coverage)
        # avg_cov = total_cov/len(self.measured_coverage)
        # print("Average analysis: ", avg_cov)
        return self.finished_cases

    def start_case(self, case, ambulances_in_motion, start_time):
        """
        Starts the case by selecting an ambulance and deploying it
        :param case:
        :param ambulances_in_motion:
        :param start_time:
        :return: True if case starts successfully; False if ambulance_selection fails to select an ambulance
        """

        print("Starting case {} which was recorded at {}".format(case.id, case.datetime))

        # Find the analysis, determine
        self.demand_coverage.calculate_coverage(self.ambulances)
        # print("Coverage: ", self.demand_coverage.get_most_recent())

        # Select ambulance to dispatch
        available_ambulances = [amb for amb in self.ambulances if not amb.deployed]
        selection = self.ambulance_selection.select_ambulance(available_ambulances, case, self.current_time)
        chosen_ambulance = selection.get('choice')
        ambulance_travel_time = selection.get('travel_time', None)

        # Dispatch an ambulance if one was found
        if chosen_ambulance is not None:

            # TODO - Currently assume that each case will take 2x travel time + 20 minutes
            # TODO - Algorithm for case duration?
            # Compute duration of the trip
            duration = ambulance_travel_time * 2 + datetime.timedelta(minutes=20)

            # Compute the end timestamp of the trip
            end_time = start_time + duration

            print('Ambulance {} chosen with one-way travel time {} (total duration: {})'.format(chosen_ambulance.id,
                                                                                                ambulance_travel_time,
                                                                                                duration))

            # Update the case with information
            case.start_time = start_time
            case.finish_time = end_time
            case.delay = case.start_time - case.datetime
            case.assigned_ambulance = chosen_ambulance

            # Deploy ambulance
            chosen_ambulance.deploy(case)
            ambulances_in_motion.append(chosen_ambulance)

            # Add case to finished cases and remove from working cases
            self.finished_cases.append(case)

            print(colored("Deploying ambulance {} at time {}".format(chosen_ambulance.id, start_time), "green"))
            print("Delay on this case: {}".format(case.delay))

            return True

        else:
            print(colored("ERROR: Algorithm failed to select an ambulance", "red"))
            return False

    def finish_ambulances(self, ambulances_in_motion, current_datetime):
        """
        Given the list of ambulances in motion, check the current time.
        Mark ambulances that have finished as non-deployed.
        :param ambulances_in_motion: A list of ambulances in motion. Want to see whether each has finished.
        :param current_datetime: The current time given as a python datetime.
        :return: None. It just changes state.
        """

        new_ambulance_list = []
        for amb in ambulances_in_motion:
            if amb.end_time <= current_datetime:
                amb.finish(amb_location=amb.base)
                print(colored('Retiring ambulance {} at time {}'.format(amb.id, amb.end_time), 'cyan'))
            else:
                new_ambulance_list.append(amb)

        return new_ambulance_list


class Event:
    START_CASE = "Start Case"
    DELAY_CASE = "Delay Case"
    RETIRE_AMBULANCE = "Retire Ambulance"
