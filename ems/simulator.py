# Runs the simulation.
from ems.algorithms.algorithm import DispatcherAlgorithm
from ems.settings import Settings
from ems.data.ambulance import Ambulance 
from ems.data.dataset import CSVTijuanaDataset

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
        
