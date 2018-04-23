# Model the data by their types.

from ems.utils import parse_headered_csv, parse_unheadered_csv
from ems.settings import Settings

from datetime import timedelta
from geopy import Point

import pandas as pd 
import datetime


class CSVTijuanaDataset ():

    def __init__ (self, settings: Settings):

        # Read files into pandas dataframes and lists of objects
        self.cases_df, self.cases                = self.read_cases(settings.cases_file)
        self.bases_df, self.bases                = self.read_bases(settings.bases_file)
        self.demands_df, self.demands            = self.read_demands(settings.demands_file)
        self.traveltimes_df, self.traveltimes    = self.read_times(settings.traveltimes_file)

        # Maybe since this is a byproduct of some algorithmic processing done with kmeans
        # we can store it in the results object?
        self.chosen_bases = []

    def read_cases(self, file):
        # Read cases from CSV into a pandas dataframe
        case_headers = ["id", "lat", "long", "date", "weekday", "time", "priority"]
        cases_df = parse_headered_csv(file, case_headers)

        # Aggregates columms 'date' and 'time' to produce a column for datetime objects
        # TODO -- SLOW OPERATION - find a better way to parse date and time to datetime object
        cases_df["datetime"] = pd.to_datetime(cases_df.date + ' ' + cases_df.time)

        # Generate list of models from dataframe
        cases = []
        for index, row in cases_df.iterrows():
            case = Case(
                id=row["id"],
                x=row["lat"],
                y=row["long"],
                dt=row["datetime"],
                weekday=row["weekday"],
                priority=row["priority"])
            cases.append(case)

        return cases_df, cases

    def read_bases(self, file):
        # Read bases from an unheadered CSV into a pandas dataframe
        base_col_positions = [4, 5]
        base_headers = ["lat", "long"]
        bases_df = parse_unheadered_csv(file, base_col_positions, base_headers)

        # Generate list of models from dataframe
        bases = []
        for index, row in bases_df.iterrows():
            base = Base(
                id=index,
                x=row["lat"],
                y=row["long"])
            bases.append(base)

        return bases_df, bases

    def read_demands(self, file):
        # Read demands from an unheadered CSV into a pandas dataframe
        demand_col_positions = [0, 1]
        demand_headers = ["lat", "long"]
        demands_df = parse_unheadered_csv(file, demand_col_positions, demand_headers)

        # Generate list of models from dataframe
        demands = []
        for index, row in demands_df.iterrows():
            demand = Demand(
                id=index,
                x=row["lat"],
                y=row["long"])
            demands.append(demand)

        return demands_df, demands

    def read_times(self, file):
        # Read travel times from CSV file into a pandas dataframe
        traveltimes_df = pd.read_csv (file)

        # Traveltimes currently stored with keys as tuples
        # e.g. traveltimes[(1, 2)]
        # Obtains the travel time object from base 1 to demand point 2
        traveltimes = {}

        # Each row represents travel times from one base to all demand points
        for base_index, row in traveltimes_df.iterrows():
            for demand_index, time in enumerate(row):

                delta = timedelta(seconds=int(time))

                traveltime = TravelTime(
                    base_id=base_index,
                    demand_id=demand_index,
                    traveltime=delta)

                traveltimes[(base_index, demand_index)] = traveltime

        return traveltimes_df, traveltimes


class Case:

    def __init__ (self, id: int, x: float, y: float, dt: datetime.datetime, 
                  weekday: str, priority: float = None, 
                  delayed: datetime = datetime.timedelta(minutes = 0)):

        self.id         = id
        self.location   = Point (x,y)
        self.weekday    = weekday
        self.datetime   = dt
        self.priority   = priority
        self.delayed    = delayed


class Base:

    def __init__ (self, id: int, x: float, y: float):

        self.id = id
        self.location = Point (x,y)


class Demand:

    def __init__ (self, id: int, x: float, y: float):

        self.id = id
        self.location = Point (x,y)


class TravelTime:

    def __init__(self, base_id: int, demand_id: int, traveltime: timedelta):

        self.base_id = base_id
        self.demand_id = demand_id
        self.traveltime = traveltime
        

