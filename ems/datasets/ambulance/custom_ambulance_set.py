from ems.datasets.ambulance.ambulance_set import AmbulanceSet
from ems.datasets.location.location_set import LocationSet
from ems.models.ambulances.ambulance import Ambulance


class CustomAmbulanceSet(AmbulanceSet):

    def __init__(self,
                 bases: LocationSet):
        self.bases = bases
        super().__init__(self.initialize_ambulances())

    def initialize_ambulances(self):
        ambulances = [Ambulance(id=str(i),
                                base=self.bases[i],
                                location=self.bases[i]) for i in range(len(self.bases))]

        return ambulances

    # def write_to_file(self, output_filename):
    #     a = [{"id": ambulance.id,
    #           "base_latitude": ambulance.base.latitude,
    #           "base_longitude": ambulance.base.longitude,
    #           "capability": ambulance.capability.value} for ambulance in self.ambulances]
    #     df = pd.DataFrame(a, columns=["id", "base_latitude", "base_longitude", "capability"])
    #     df.to_csv(output_filename, index=False)

    def __len__(self):
        return len(self.bases)
