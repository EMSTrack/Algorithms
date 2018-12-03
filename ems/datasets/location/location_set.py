import pandas as pd
from typing import List

from geopy import Point


class LocationSet:

    def __init__(self, locations: List[Point]):
        self.locations = locations

    def __len__(self):
        return len(self.locations)

    def closest(self, point: Point):
        raise NotImplementedError()

    def write_to_file(self, output_filename: str):
        a = [{"latitude": location.latitude,
              "longitude": location.longitude} for location in self.locations]
        df = pd.DataFrame(a, columns=["latitude", "longitude"])
        df.to_csv(output_filename, index=False)
