# Runs the simulation.
from ems.models.ambulance import Ambulance 
from ems.algorithms.algorithm import DispatcherAlgorithm
from ems.settings import Settings
from ems.data import Data

class DispatcherSimulator():

    def __init__ (self, settings, data, algorithm):

        assert isinstance (settings, Settings)
        assert isinstance (data, Data)
        assert isinstance (algorithm, DispatcherAlgorithm)

        self.settings = settings
        self.data = data
        self.algorithm = algorithm

    def run (self):
        
        chosen_bases = self.algorithm.init_bases(self.data)
        
