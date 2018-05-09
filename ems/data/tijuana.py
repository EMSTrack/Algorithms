# Model the data by their types.

import os
import pandas as pd
from geopy import Point

from ems.data.dataset import Dataset
from ems.data.traveltimes import TravelTimes
from ems.models.base import Base
from ems.models.case import Case
from ems.models.demand import Demand
from ems.models.location_set import LocationSet
from ems.utils import parse_headered_csv, parse_unheadered_csv


class CSVTijuanaDataset(Dataset):

    def __init__(self,
                 demands_filepath: str,
                 bases_filepath: str,
                 cases_filepath: str,
                 traveltimes_filepath: str):

        # Read files into pandas dataframes and lists of objects
        self.demands, self.demands_df = self.read_demands(demands_filepath)
        self.bases, self.bases_df = self.read_bases(bases_filepath)
        self.cases, self.cases_df = self.read_cases(cases_filepath)



        # TODO
        self.basesLS = LocationSet(self.bases)
        self.demandsLS = LocationSet(self.demands)

        self.traveltimes, self.traveltimes_df = self.read_times(traveltimes_filepath)

        # self.traveltimes = TravelTimes(self.basesLS, self.demandsLS, )


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
            case = Case(
                id=row["id"],
                point=Point(row["lat"], row["long"]),
                dt=row["datetime"],
                weekday=row["weekday"],
                priority=row["priority"])
            cases.append(case)

        return cases, cases_df

    def read_bases(self, filename):
        # Read bases from an unheadered CSV into a pandas dataframe
        base_col_positions = [4, 5]
        base_headers = ["lat", "long"]
        bases_df = parse_unheadered_csv(filename, base_col_positions, base_headers)

        # Generate list of models from dataframe
        bases = []
        for index, row in bases_df.iterrows():
            base = Base(
                id=index,
                point=Point(row["lat"], row["long"])
            )
            bases.append(base)

        return bases, bases_df

    def read_demands(self, filename):
        # Read demands from an unheadered CSV into a pandas dataframe
        demand_col_positions = [0, 1]
        demand_headers = ["lat", "long"]
        demands_df = parse_unheadered_csv(filename, demand_col_positions, demand_headers)

        # Generate list of models from dataframe
        demands = []
        for index, row in demands_df.iterrows():
            demand = Demand(
                id=index,
                point=Point(row["lat"], row["long"])
            )
            demands.append(demand)

        return demands, demands_df

    def read_times(self, filename):
        # Read travel times from CSV file into a pandas dataframe
        traveltimes_df = pd.read_csv(filename)
        # import IPython; IPython.embed()


        traveltimes = TravelTimes(self.basesLS, self.demandsLS, traveltimes_df.as_matrix())

        return traveltimes, traveltimes_df

    # Implementation
    def get_bases(self):
        return self.bases

    def get_cases(self):
        return self.cases

    def get_demands(self):
        return self.demands
