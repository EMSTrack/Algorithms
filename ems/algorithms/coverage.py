# Framework for using algorithms and allowing for replacement
from typing import List

from ems.models.ambulance import Ambulance
from ems.models.case import Case
from ems.models.location_set import LocationSet
from ems.models.demand import Demand


# Used by the sim to select ambulances
class CoverageAlgorithm:
    """
        Barebone class. Users may subclass to implement their own algorithm for
        finding coverage.
    """

    # TODO This may not even be the right signature.
    def calculateCoverage(self,
                         demands: LocationSet,
                         ambulances: List[Ambulance]):
        """
        The signature for the function which runs the coverage algorithm
        :param demands: 
        :param ambulances:
        :return:
        """
        raise NotImplementedError()
