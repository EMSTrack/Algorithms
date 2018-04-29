# Runs the simulation.

import datetime
from copy import deepcopy
from typing import List

from colorama import Fore
from colorama import Style

from ems.algorithms.algorithm import Algorithm
from ems.models.ambulance import Ambulance
from ems.models.base import Base
from ems.models.case import Case
from ems.models.demand import Demand
from ems.simulators.simulator import Simulator


class DispatcherSimulator(Simulator):

    def __init__(self,
                 ambulances: List[Ambulance],
                 bases: List[Base],
                 cases: List[Case],
                 demands: List[Demand],
                 algorithm: Algorithm):

        self.finished_cases = []
        self.working_cases = deepcopy(cases)
        self.current_time = cases[0].datetime if len(cases) > 0 else -1
        super(DispatcherSimulator, self).__init__(ambulances, bases, cases, demands, algorithm)

    def run(self):

        ambulances_in_motion = []

        # TODO. This may become a while-loop, "while there are still start times and end times..."
        while self.working_cases or ambulances_in_motion:

            print()
            print("Current time: {}".format(self.current_time))

            # If no more cases to start, finish all cases that are currently being handled by
            # the ambulances
            if not self.working_cases:
                for amb in ambulances_in_motion:
                    amb.finish()

                # TODO Find the city coverage. Is it useful to check the coverage within the loop? This would be
                # TODO the only place where such a granular measurement is present.

                # TODO -- save amortized file

                return self.finished_cases

            # Start the first case
            elif not ambulances_in_motion and self.working_cases:

                # Retrieve first case
                next_case = self.working_cases[0]

                # Set the current time based on the start time of the first case
                self.current_time = next_case.datetime

                # Deploy an ambulance to handle the current case
                self.start_case(next_case, ambulances_in_motion, self.current_time)

                # TODO If the deployment was successful, then recalculate the city coverage

            elif ambulances_in_motion and self.working_cases:

                # Sort all ambulances by their end times
                ambulances_in_motion = sorted(ambulances_in_motion, key=lambda k: k.end_time)

                # Retrieve next case
                next_case = self.working_cases[0]
                case_start_time = next_case.datetime

                # If all ambulances are taken - must fast forward time until next ambulance is released
                if len(self.ambulances) == len(ambulances_in_motion):

                    print("No available ambulances")

                    next_available_amb = ambulances_in_motion[0]
                    ambulance_release_time = next_available_amb.end_time

                    print("Soonest release time for an ambulance: Ambulance {} at {}".format(next_available_amb.id,
                                                                                             ambulance_release_time))

                    # Fast forward current time to be when the next ambulances gets released
                    self.current_time = ambulance_release_time

                    # Finish the ambulance
                    ambulances_in_motion = self.finish_ambulances(ambulances_in_motion, self.current_time)

                # Can't start case because it has not happened yet
                elif case_start_time > self.current_time:

                    # Fast forward current time to be when the next case starts
                    self.current_time = case_start_time

                    # Finish ambulances whose trips have ended during this fast forward
                    ambulances_in_motion = self.finish_ambulances(ambulances_in_motion, self.current_time)

                # Can start the next case
                else:
                    # Start the next case at current time
                    self.start_case(next_case, ambulances_in_motion, self.current_time)

                # Compute coverage
                # self.coverage (ambulances, self.traveltimes, self.bases, self.demands, required_r1)

            else:
                raise Exception("This shouldn't happen... ")

        # TODO return "results" object with more potential information
        return self.finished_cases

    def start_case(self, case, ambulances_in_motion, start_time):
        """
        Actual code to attempt running the case.
        :param case:
        :param ambulances_in_motion:
        :param start_time:
        :return: True if case starts successfully, false if no ambulances available.
        (This may not actually be necessary since I don't use this boolean in the preceding fn)
        """

        print("Starting case {} which was recorded at {}".format(case.id, case.datetime))

        # TODO access amortized case->demand mappings

        # Select ambulance to dispatch
        chosen_ambulance, ambulance_travel_time = \
            self.algorithm.select_ambulance(self.ambulances, case, self.demands)

        # Dispatch an ambulance as returned by find_available. It only works if deployed
        if chosen_ambulance is not None:

            # Obtain ambulance
            ambulance = self.ambulances[chosen_ambulance]

            print('Ambulance {} chosen with travel time duration {}'.format(ambulance.id,
                                                                            ambulance_travel_time))

            # TODO I assume that each case will take 2x travel time + 20 minutes
            # Compute duration of the trip
            duration = ambulance_travel_time * 2 + datetime.timedelta(minutes=20)

            # Compute the end timestamp of the trip
            end_time = start_time + duration

            print('Final computed case duration: {}'.format(duration))

            # TODO -- fill in destination?
            # Deploy ambulance
            ambulance.deploy(start_time, None, end_time)
            ambulances_in_motion.append(ambulance)

            # Set case start + finish timestamps and the case delay
            case.start_time = start_time
            case.finish_time = end_time
            case.delay = case.start_time - case.datetime

            # Add case to finished cases and remove from working cases
            self.finished_cases.append(case)
            self.working_cases.pop(0)

            print(f"{Fore.GREEN}Deploying ambulance", ambulance.id, 'at time', start_time, f'{Style.RESET_ALL}')
            print("Delay on this case: {}".format(case.delay))

            return True

        else:
            print("ERROR: Algorithm failed to select an ambulance")

    def finish_ambulances(self, ambulances_in_motion, current_datetime):
        """
        Given the list of ambulances in motion, check the current time.
        Mark ambulances that have finished as non-deployed.
        :param ambulances_in_motion: A list of ambulances in motion. Want to see whether each has finished.
        :param current_datetime: The current time given as a python datetime.
        :param ambulance_delta: The amount of time the case should take. Could get complicated upon CSE 199 link.
        :return: None. It just changes state.
        """

        print(f"Busy ambulances:", sorted([amb.id for amb in ambulances_in_motion]), f"{Style.RESET_ALL}")

        new_ambulance_list = []
        for amb in ambulances_in_motion:
            if amb.end_time <= current_datetime:
                amb.finish()
                print(f'{Fore.CYAN}Retiring ambulance ', amb.id, 'at time', amb.end_time,
                      f"{Style.RESET_ALL}")
            else:
                new_ambulance_list.append(amb)

        return new_ambulance_list

    # def coverage(ambulances, times, bases, demands,  required_r1):
    #     # Mark all demands which has a base less than r1 traveltime away as covered. 
    #     # In the future, r1 travelttime of ambulance.

    #     # Then, return the percentage of Tijuana covered.
    #     # Parameters: ambulances, bases, demands, traveltimes, r1.

    #     # print("Recalculate the city coverage. ")

    #     # As long as amb['deployed'] in ambulances is false, the base can have coverage effect.
    #     # print("Bases:", len (bases))
    #     # print("Demands:", len (demands))
    #     # print("r1:", required_r1)

    #     # Which bases cast a coverage effect over a part of the city?
    #     # amb['base'] == base in bases
    #     # print(ambulances[0])

    #     # from IPython import embed; embed()

    #     uncovered_demands = [0 for d in demands]

    #     # print("Find nonempty bases...")
    #     nonempty_bases = [amb.base for amb in ambulances if amb.deployed == False]
    #     # for base in bases:
    #         # for amb in ambulances:
    #             # if base == amb['base'] and amb['deployed'] == False and base not in nonempty_bases:
    #                 # nonempty_bases.append(base)

    #     # print("Calculate coverage rating... ", len(nonempty_bases)*len(demands))
    #     for active_base in nonempty_bases:
    #         for d in range(len(demands)):
    #             if uncovered_demands [d] == 0:
    #                 if traveltime(times, bases, demands, active_base, demands [d]).total_seconds() < required_r1:
    #                     uncovered_demands[d] = 1

    #     # from IPython import embed; embed ()
    #     print(f"{Fore.RED}Coverage Rating:", sum(uncovered_demands), "/100.",  f'{Style.RESET_ALL}')
    #     return sum (uncovered_demands)
