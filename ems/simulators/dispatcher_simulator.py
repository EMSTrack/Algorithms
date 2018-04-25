# Runs the simulation.

import datetime
from copy import deepcopy
from typing import List

from ems.algorithms.algorithm import DispatcherAlgorithm
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
                 algorithm: DispatcherAlgorithm):

        super(DispatcherSimulator, self).__init__(ambulances, bases, cases, demands, algorithm)

    def run(self):

        # initialize time
        time = 0

        working_cases = deepcopy(self.cases)
        finished_cases = []
        ambulances_in_motion = []

        # TODO. This may become a while-loop, "while there are still start times and end times..."
        while working_cases or ambulances_in_motion:

            # if self.settings.debug: print()

            # What is the next timestep?
            # If no more cases to start, then there should only be ambulances left.

            if not working_cases:
                for amb in ambulances_in_motion:
                    amb.finish()

                # TODO Find the city coverage. Is it useful to check the coverage within the loop? This would be
                # TODO the only place where such a granular measurement is present.

                # TODO -- save amortized file

                return finished_cases

            elif not ambulances_in_motion and working_cases:
                start_time = working_cases[0].datetime

                # Deploy
                self.start_case(finished_cases, working_cases, self.ambulances, ambulances_in_motion, start_time)

                # TODO If the deployment was successful, then recalculate the city coverage

            elif ambulances_in_motion and working_cases:

                # Compare the earlier case of the two
                ambulances_in_motion = sorted(ambulances_in_motion, key=lambda k: k.end_time)
                ambulance_release_time = ambulances_in_motion[0].end_time
                case_start_time = working_cases[0].datetime
                delta = working_cases[0].delayed

                # print ("ambulance_time", ambulance_release_time)
                # print ("case_time     ", case_start_time + delta)

                if case_start_time + delta < ambulance_release_time:
                    # Deploy
                    self.start_case(finished_cases, working_cases, self.ambulances, ambulances_in_motion,
                                    case_start_time + delta)

                    # TODO If the deployment was successful, then recalculate the city coverage

                else:
                    self.check_finished_ambulances(ambulances_in_motion, ambulance_release_time)

                # Compute coverage
                # self.coverage (ambulances, self.traveltimes, self.bases, self.demands, required_r1)

            else:
                raise Exception("This shouldn't happen... ")

        # TODO return "results" object with more potential information
        return finished_cases

    def start_case(self, finished_cases, working_cases, ambulances, ambulances_in_motion, start_time):
        """
        Actual code to attempt running the case.
        :param finished_cases:
        :param working_cases:
        :param ambulances:
        :param ambulances_in_motion:
        :param start_time:
        :return: True if case starts successfully, false if no ambulances available.
        (This may not actually be necessary since I don't use this boolean in the preceding fn)
        """

        case = working_cases[0]
        # if self.settings.debug: print(case.id)

        # Checks if the previously dispatched ambulances are done. If so, mark as done.
        self.check_finished_ambulances(ambulances_in_motion, start_time)

        # TODO access amortized case->demand mappings

        # Select ambulance
        chosen_ambulance, ambulance_travel_time = \
            self.algorithm.select_ambulance(ambulances, case, self.demands, self.algorithm.traveltimes)

        # if self.settings.debug: print('chosen_ambulance:', chosen_ambulance)
        # if self.settings.debug: print('travel time duration:', ambulance_travel_time)

        # Dispatch an ambulance as returned by fine_available. It only works if deployed
        if chosen_ambulance is not None:
            # TODO I assume that each case will take 2x travel time + 20 minutes
            case_time = ambulance_travel_time * 2 + datetime.timedelta(minutes=20)

            ambulance = ambulances[chosen_ambulance]

            # TODO -- fill in destination?
            #if self.settings.debug: print(f"{Fore.GREEN}Deploying ambulance", ambulance.id, 'at time', case_time,
            #                              f'{Style.RESET_ALL}')

            ambulance.deploy(start_time, None, case_time)
            ambulances_in_motion.append(ambulance)

            finished_cases.append(case)
            working_cases.remove(case)

            return True

        else:
            #if self.settings.debug: print(
            #    f"{Fore.RED}***** THIS CASE HAS BEEN DELAYED BY ONE MINUTE. *****\n{Style.RESET_ALL}")
            case.delayed = datetime.timedelta(minutes=1, seconds=case.delayed.total_seconds())
            # working_cases.insert(0, case)
            return False

    def check_finished_ambulances(self, ambulances_in_motion, current_datetime):
        """
        Given the list of ambulances in motion, check the current time.
        Mark ambulances that have finished as non-deployed.
        :param ambulances_in_motion: A list of ambulances in motion. Want to see whether each has finished.
        :param current_datetime: The current time given as a python datetime.
        :param ambulance_delta: The amount of time the case should take. Could get complicated upon CSE 199 link.
        :return: None. It just changes state.
        """

        #if self.settings.debug: print(f"Busy ambulances:", sorted([amb.id for amb in ambulances_in_motion]),
        #                              f"{Style.RESET_ALL}")

        # Watch out, never remove from list while iterating through it
        for ambulance in ambulances_in_motion:
            if ambulance.end_time <= current_datetime:  # TODO

                ambulances_in_motion.remove(ambulance)

                #if self.settings.debug: print(f'{Fore.CYAN}Retiring ambulance ', ambulance.id, 'at time',
                #                              current_datetime,
                #                              f"{Style.RESET_ALL}")

                ambulance.finish()

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
