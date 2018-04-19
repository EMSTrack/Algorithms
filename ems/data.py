# Model the data by their types.

from geopy import Point
import pandas as pd 
from ems.settings import Settings

class Data ():

    def __init__ (self, 
        settings):

        assert isinstance (settings, Settings)

        # TODO -- I actually think traveltimes should go in the ambulance class.
        # self.traveltimes = self.file_to_traveltimes() 

        self.cases     = self.read_cases(settings.cases_file)
        self.bases     = self.read_bases(settings.bases_file)
        self.demands   = self.read_demands(settings.demands_file)

        self.chosen_bases = [] # TODO algorithm.init_bases()?


    def read_cases(self, file):
        case_headers = ["id", "lat", "long", "date", "weekday", "time", "priority"]
        cases_raw = self.parse_csv(file, case_headers)
        # TODO parse into object
        return cases_raw

    def read_bases(self, file):
        base_headers = ["lat", "long"]
        bases_raw = self.parse_csv(file, base_headers)
        # TODO parse into object
        return bases_raw

    def read_demands(self, file):
        demand_headers = ["lat", "long"]
        demands_raw = self.parse_csv(file, demand_headers)
        # TODO parse into object
        return demands_raw

    def parse_csv (self, file, desired_keys):

        assert file is not None
        assert file is not ""
        assert isinstance (file, str)
        assert isinstance (desired_keys, list)
        assert all(isinstance(ele, str) for ele in desired_keys)

        raw = pd.read_csv (file)

        keys_read = raw.keys()

        for key in desired_keys:
            if key not in keys_read:
                raise Exception("{} was not found in keys of file {}".format(key, file))

        return raw[desired_keys]



class Case ():

    # TODO brainstorm optional params
    def __init__ (self, id, x, y, date, weekday, time, priority):

        assert isinstance(id, int)
        assert isinstance(x, float)
        assert isinstance(y, float)
        # TODO finish asserts
        # assert isinstance(date, )
        # assert isinstance(weekday, )
        # assert isinstance(time, )
        # assert isinstance(priority, )

        self.id         = id
        self.location   = Point (x,y)
        self.date       = date
        self.weekday    = weekday
        self.time       = time
        self.priority   = priority


class Base ():

    def __init__ (self, x, y):
        
        assert isinstance(x, float)
        assert isinstance(y, float)

        self.location = Point (x,y)


class Demand ():

    def __init__ (self, x, y):

        assert isinstance(x, float)
        assert isinstance(y, float)

        self.location = Point (x,y)


class TravelTime ():

    def __init__(self):
        pass


    def getTime (base, demand):
        pass
