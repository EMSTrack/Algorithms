from geopy import Point

from ems.datasets.location.kd_tree_location_set import KDTreeLocationSet
from ems.utils import parse_unheadered_csv


class TijuanaBaseSet(KDTreeLocationSet):

    def __init__(self, filename):
        super().__init__(self.read_bases(filename))

    def read_bases(self, filename):
        # Read bases from an unheadered CSV into a pandas dataframe
        base_col_positions = [4, 5]
        base_headers = ["lat", "long"]
        bases_df = parse_unheadered_csv(filename, base_col_positions, base_headers)

        # Generate list of models from dataframe
        bases = []
        for index, row in bases_df.iterrows():
            base = Point(row["lat"], row["long"])
            bases.append(base)

        return bases
