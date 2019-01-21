import pandas as pd

from ems.datasets.location.location_set import LocationSet
from ems.datasets.travel_times.travel_times import TravelTimes


class TijuanaTravelTimes(TravelTimes):

    def __init__(self,
                 origins: LocationSet,
                 destinations: LocationSet,
                 filename: str):
        """
        :param origins:
        :param destinations:
        :param filename:
        """
        times = self.read_times_df(filename)
        super().__init__(origins, destinations, times)

    def read_times_df(self, filename):
        # Read travel travel_times from CSV file into a pandas dataframe
        travel_times_df = pd.read_csv(filename)

        return travel_times_df.as_matrix()
