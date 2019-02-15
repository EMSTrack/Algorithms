from ems.algorithms.base_selectors.selector import AmbulanceBaseSelector
from ems.datasets.location.location_set import LocationSet


class TijuanaBaseSelector(AmbulanceBaseSelector):
    """ Assigned ambulances to bases in round robin order.  """

    def __init__(self,
                 base_set: LocationSet):
        self.base_set = base_set

    def select(self, num_ambulances):



        no_ambulances = [-6]
        one_ambulances = [i for i in range(-8, 0) if i not in no_ambulances]
        two_ambulances = [-8, -7, -4, -1]

        ambulances = one_ambulances + two_ambulances

        bases = []

        for base_index in ambulances:
            bases.append(self.base_set.locations[base_index])

        if len(bases) != num_ambulances:
            raise Exception("Wrong number of bases were being assigned to ambulances.")

        return bases
