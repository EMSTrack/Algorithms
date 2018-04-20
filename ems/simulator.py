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

        # Assign ambulances to bases chosen
        ambulance_bases = self.algorithm.init_ambulance_placements(chosen_bases, 
        														  self.settings.num_ambulances)

        print([base.location for base in ambulance_bases])

        # TODO generate ambulance objects?
        
