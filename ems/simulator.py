# Runs the simulation.

import datetime
from copy import deepcopy

from colorama import Fore
from colorama import Style

from ems.algorithms.algorithm import DispatcherAlgorithm
from ems.data.tijuana import CSVTijuanaDataset
from ems.models.ambulance import Ambulance
from ems.settings import Settings


class Simulator:

    def __init__(self,
                 bases,
                 ambulances,
                 cases,
                 algorithm: DispatcherAlgorithm):

        self.bases = bases
        self.ambulances = ambulances
        self.cases = cases
        self.algorithm = algorithm

    def run(self):

        # get number of ambulances
        number_of_ambulances = len(self.ambulances)

        # initialize time
        time = 0

        working_cases = deepcopy(self.cases)
        finished_cases = []
        ambulances_in_motion = []

        # TODO. This may become a while-loop, "while there are still start times and end times..."
        while working_cases or ambulances_in_motion:

            if self.settings.debug: print()

            # What is the next timestep?
            # If no more cases to start, then there should only be ambulances left.

            if not working_cases:
                for amb in ambulances_in_motion:
                    amb.finish(time)

                # TODO Find the city coverage. Is it useful to check the coverage within the loop? This would be
                # TODO the only place where such a granular measurement is present.

                # TODO -- save amortized file

                return finished_cases

            elif not ambulances_in_motion and working_cases:
                start_time = working_cases[0].datetime

                # Deploy
                self.start_case(finished_cases, working_cases, ambulances, ambulances_in_motion, start_time)

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
                    self.start_case(finished_cases, working_cases, ambulances, ambulances_in_motion,
                                    case_start_time + delta)

                    # TODO If the deployment was successful, then recalculate the city coverage

                else:
                    self.check_finished_ambulances(ambulances_in_motion, ambulance_release_time)

                # Compute coverage
                # coverage (ambulances, self.dataset.traveltimes, self.dataset.bases, \
                #     self.dataset.demands, required_r1)

            else:
                raise Exception("This shouldn't happen... ")

        # TODO return "results" object with more potential information
        return finished_cases

    def start_case(self, finished_cases, working_cases, ambulances, ambulances_in_motion, start_time):
        pass

    def check_finished_ambulances(self, ambulances_in_motion, current_datetime):
        pass
