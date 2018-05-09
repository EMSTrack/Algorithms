# Framework for using algorithms and allowing for replacement
from typing import List

from ems.models.ambulance import Ambulance
from ems.models.location_set import LocationSet


# Used by the sim to select ambulances
class CoverageAlgorithm:
    """
        Barebone class. Users may subclass to implement their own ambulance_selection for
        finding coverage.
    """

    # TODO This may not even be the right signature.
    def calculateCoverage(self,
                          demands: LocationSet,
                          ambulances: List[Ambulance]):
        """
        The signature for the function which runs the coverage ambulance_selection
        :param demands:
        :param ambulances:
        :return:
        """
        raise NotImplementedError()
