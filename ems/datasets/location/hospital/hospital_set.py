from typing import List

from ems.datasets.location.kd_tree_location_set import KDTreeLocationSet
from ems.utils import parse_unheadered_csv


class HospitalSet(KDTreeLocationSet):

    def __init__(self,
                 filename: str = None,
                 latitudes: List[float] = None,
                 longitudes: List[float] = None):
        if filename is not None:
            latitudes, longitudes = self.read_hospitals(filename)
        super().__init__(latitudes, longitudes)

    def read_hospitals(self, filename):
        # Read hospitals from an unheadered CSV into a pandas dataframe
        hospital_col_positions = [0, 1]
        hospital_headers = ["lat", "long"]
        hospitals_df = parse_unheadered_csv(filename, hospital_col_positions, hospital_headers)

        # Generate list of models from dataframe
        latitudes = []
        longitudes = []
        for index, row in hospitals_df.iterrows():
            latitudes.append(row["lat"])
            longitudes.append(row["long"])

        return latitudes, longitudes
