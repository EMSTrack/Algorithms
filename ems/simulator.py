# Runs the simulation.
from ems.algorithms.algorithm import DispatcherAlgorithm
from ems.settings import Settings
from ems.data.ambulance import Ambulance 
from ems.data.dataset import CSVTijuanaDataset

from colorama import Fore
from colorama import Style

import datetime

class DispatcherSimulator():

    def __init__ (self, settings, dataset, algorithm):

        assert isinstance (settings, Settings)
        assert isinstance (dataset, CSVTijuanaDataset)
        assert isinstance (algorithm, DispatcherAlgorithm)

        self.settings = settings
        self.dataset = dataset
        self.algorithm = algorithm

    def run (self):
        
        # Select bases from dataset
        chosen_bases = self.algorithm.init_bases(self.dataset)

        # Maybe not necessary
        self.dataset.chosen_bases = chosen_bases

        # Assign ambulances to bases chosen
        ambulance_bases = self.algorithm.init_ambulance_placements(chosen_bases, 
                                                                  self.settings.num_ambulances)

        # Generate ambulances; Does not have to be here
        ambulances = []
        for index in range(self.settings.num_ambulances):
            ambulance = Ambulance(id=index,
                                  base=ambulance_bases[index])
            ambulances.append(ambulance)

        # TODO - Amortized file

        working_cases = deepcopy(self.dataset.bases)
        finished_cases = []
        ambulances_in_motion = []

        # TODO. This may become a while-loop, "while there are still start times and end times..."
        while working_cases or ambulances_in_motion:
            if debug: print()

            # What is the next timestep?
            # If no more cases to start, then there should only be ambulances left.

            if not working_cases:
                for amb in ambulances_in_motion:
                    amb.finish(amb.end_time)

                # TODO Find the city coverage. Is it useful to check the coverage within the loop? This would be
                # TODO the only place where such a granular measurement is present.

                # TODO -- save amortized file


                return finished_cases

            elif not not ambulances_in_motion and working_cases:
                start_time = working_cases[0].datetime
                # TODO -- Deploy
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
                    # TODO -- Deploy
                    # TODO If the deployment was successful, then recalculate the city coverage

                else:
                    self.check_finished_ambulances(ambulances_in_motion, ambulance_release_time)

                # TODO traveltime coverage

            else:
                raise Exception("This shouldn't happen... ")

        # TODO return "results" object with more potential information
        return finished_cases

    def start_case(finished_cases, working_cases, ambulances, ambulances_in_motion, start_time):
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
        if debug: print(case.id)

        # Checks if the previously dispatched ambulances are done. If so, mark as done.
        self.check_finished_ambulances(ambulances_in_motion, start_time)

        target_point = case.location
        case_id = case.id

        closest_location = None

        # TODO access amortized case->demand mappings
        # TODO compute traveltime closest distance

        if debug: print ('chosen_ambulance:', chosen_ambulance)
        if debug: print ('travel time duration:', ambulance_travel_time)

        # Dispatch an ambulance as returned by fine_available. It only works if deployed
        if chosen_ambulance is not None:
            # TODO I assume that each case will take 2x travel time + 20 minutes
            case_time = ambulance_travel_time * 2 + datetime.timedelta(minutes=20)

            ambulance = ambulances[chosen_ambulance]

            # TODO -- destination?
            ambulance.deploy(start_time, None, case_time)
            ambulances_in_motion.append(ambulance)

            finished_cases.append(case)
            working_cases.remove(case)

            return True

        else:
            case.delayed = datetime.timedelta(minutes=1, seconds=case.delayed.total_seconds())
            # working_cases.insert(0, case)
            return False


    def check_finished_ambulances(ambulances_in_motion, current_datetime):
        """
        Given the list of ambulances in motion, check the current time.
        Mark ambulances that have finished as non-deployed.
        :param ambulances_in_motion: A list of ambulances in motion. Want to see whether each has finished.
        :param current_datetime: The current time given as a python datetime.
        :param ambulance_delta: The amount of time the case should take. Could get complicated upon CSE 199 link.
        :return: None. It just changes state.
        """

        if debug: print(f"Busy ambulances:", sorted([amb.id for amb in ambulances_in_motion]),f"{Style.RESET_ALL}")

        for ambulance in ambulances:
            if (ambulance.end_time) <= current_datetime: #TODO

                ambulances_in_motion.remove(ambulance)
                ambulance.finish(current_datetime)
