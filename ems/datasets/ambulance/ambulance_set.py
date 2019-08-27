import pandas as pd
from geopy import Point

from ems.models.ambulances.ambulance import Ambulance
from ems.models.ambulances.capability import Capability
from ems.utils import parse_headered_csv


class AmbulanceSet:

    def __init__(self,
                 ambulances=None,
                 filename=None,
                 headers=None):

        self.headers = headers

        if headers is None:
            self.headers = ["id", "base_latitude", "base_longitude", "capability"]

        if filename is not None:
            ambulances = self.read(filename)

        self.filename = filename
        self.ambulances = ambulances

    def __len__(self):
        return len(self.ambulances)

    def write_to_file(self, output_filename):
        a = [{"id": ambulance.identifier,
              "base_latitude": ambulance.base.latitude,
              "base_longitude": ambulance.base.longitude,
              "capability": ambulance.capability.name} for ambulance in self.ambulances]
        df = pd.DataFrame(a, columns=self.headers)
        df.to_csv(output_filename, index=False)

    def read(self, filename):

        # Read ambulance from a headered CSV into a pandas dataframe
        ambulances_df = parse_headered_csv(filename, self.headers)

        # TODO -- generalize
        id_key = self.headers[0]
        b_latitude_key = self.headers[1]
        b_longitude_key = self.headers[2]
        capability_key = self.headers[3]

        # Generate list of models from dataframe
        a = []
        for _, row in ambulances_df.iterrows():
            base = Point(row[b_latitude_key],
                         row[b_longitude_key])
            ambulance = Ambulance(identifier=row[id_key],
                                  base=base,
                                  capability=Capability[row[capability_key]])
            a.append(ambulance)

        return a

