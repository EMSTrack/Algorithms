# Model the data by their types.

import pandas as pd
from geopy import Point

from ems.data.dataset import Dataset
from ems.data.travel_times import TravelTimes
from ems.models.location_set import LocationSet
from ems.models.tijuana_case import TijuanaCase
from ems.utils import parse_headered_csv, parse_unheadered_csv


class CSVTijuanaDataset(Dataset):

    def __init__(self,
                 demands_file_path: str,
                 bases_file_path: str,
                 cases_file_path: str,
                 travel_times_file_path: str):

        # Read files into pandas dataframes and lists of objects
        self.demands = self.read_demands(demands_file_path)
        self.bases = self.read_bases(bases_file_path)
        self.cases = self.read_cases(cases_file_path)

        travel_times_df = self.read_times_df(travel_times_file_path)

        self.travel_times = TravelTimes(loc_set_1=self.bases,
                                        loc_set_2=self.demands,
                                        times=travel_times_df.as_matrix())

    # Helper functions
    def read_cases(self, filename):
        # Read cases from CSV into a pandas dataframe
        case_headers = ["id", "lat", "long", "date", "weekday", "time", "priority"]
        cases_df = parse_headered_csv(filename, case_headers)

        # Aggregates columms 'date' and 'time' to produce a column for datetime objects
        # TODO -- SLOW OPERATION - find a better way to parse date and time to datetime object
        cases_df["datetime"] = pd.to_datetime(cases_df.date + ' ' + cases_df.time)

        # Sorts all cases by their datetimes (REQUIRED BY SIMULATOR)
        cases_df = cases_df.sort_values('datetime', ascending=True)

        # Generate list of models from dataframe
        cases = []
        for index, row in cases_df.iterrows():
            case = TijuanaCase(
                id=row["id"],
                location=Point(row["lat"], row["long"]),
                time=row["datetime"],
                weekday=row["weekday"],
                priority=row["priority"])
            cases.append(case)

        return cases

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

        return LocationSet(bases)

    def read_demands(self, filename):
        # Read demands from an unheadered CSV into a pandas dataframe
        demand_col_positions = [0, 1]
        demand_headers = ["lat", "long"]
        demands_df = parse_unheadered_csv(filename, demand_col_positions, demand_headers)

        # Generate list of models from dataframe
        demands = []
        for index, row in demands_df.iterrows():
            demand = Point(row["lat"], row["long"])
            demands.append(demand)

        return LocationSet(demands)

    def read_times_df(self, filename):
        # Read travel times from CSV file into a pandas dataframe
        travel_times_df = pd.read_csv(filename)

        return travel_times_df

    # Implementation
    def get_cases(self):
        return self.cases
