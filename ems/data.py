# Model the data by their types.

from geopy import Point
from ems.utils import parse_headered_csv, parse_unheadered_csv
from ems.settings import Settings

import pandas as pd 
import datetime

class CSVTijuanaData ():

    def __init__ (self, 
        settings):

        assert isinstance (settings, Settings)

        self.cases       = self.read_cases(settings.cases_file)
        self.bases       = self.read_bases(settings.bases_file)
        self.demands     = self.read_demands(settings.demands_file)
        self.traveltimes = self.read_times(settings.traveltimes_file)

        # I don't think this should be a field for data - instead since it is a byproduct
        # of some processing done with kmeans, we can store it in some "results" class
        # self.chosen_bases = []

    def read_cases(self, file):
        case_headers = ["id", "lat", "long", "date", "weekday", "time", "priority"]
        cases_df = parse_headered_csv(file, case_headers)

        # SLOW OPERATION - find a better way to parse to datetime
        cases_df.datetime = pd.to_datetime(cases_df.date + ' ' + cases_df.time)

        return cases_df

    def read_bases(self, file):
        base_col_positions = [4, 5]
        base_headers = ["lat", "long"]
        bases_df = parse_unheadered_csv(file, base_col_positions, base_headers)
        return bases_df

    def read_demands(self, file):
        demand_col_positions = [0, 1]
        demand_headers = ["lat", "long"]
        demands_df = parse_unheadered_csv(file, demand_col_positions, demand_headers)
        return demands_df

    def read_times(self, file):
        times_df = pd.read_csv (file)
        return times_df

class Case:

    def __init__ (self, id, x, y, dt, weekday, priority=None):

        assert isinstance(id, int)
        assert isinstance(x, float)
        assert isinstance(y, float)
        assert isinstance(dt, datetime)
        assert isinstance(weekday, str)
        assert isinstance(priority, float)

        self.id         = id
        self.location   = Point (x,y)
        self.weekday    = weekday
        self.datetime   = dt
        self.priority   = priority

class Base:

    def __init__ (self, x, y):
        
        assert isinstance(x, float)
        assert isinstance(y, float)

        self.location = Point (x,y)

class Demand:

    def __init__ (self, x, y):

        assert isinstance(x, float)
        assert isinstance(y, float)

        self.location = Point (x,y)

class TravelTime:

    def __init__(self):
        pass

    def getTime (base, demand):
        pass

