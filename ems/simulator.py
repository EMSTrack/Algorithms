# Runs the simulation.
from ems.algorithms.algorithm import DispatcherAlgorithm
from ems.settings import Settings
from ems.data.ambulance import Ambulance 
from ems.data.dataset import Dataset

class DispatcherSimulator():

    def __init__ (self, settings, dataset, algorithm):

        assert isinstance (settings, Settings)
        assert isinstance (dataset, Dataset)
        assert isinstance (algorithm, DispatcherAlgorithm)

        self.settings = settings
        self.dataset = dataset
        self.algorithm = algorithm

    def run (self):
        
        chosen_bases = self.algorithm.init_bases(self.dataset)
        
