# Framework for using algorithms and allowing for replacement
from typing import List

from ems.models.ambulance import Ambulance


# Used by the sim to select ambulances
class CoverageAlgorithm:
    """
    Users may subclass to implement their own analysis algorithm
    """

    def calculate(self, ambulances: List[Ambulance]):
        """
        The signature for the function which calculates analysis
        :param ambulances:
        :return:
        """
        raise NotImplementedError()
