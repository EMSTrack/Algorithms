# Model the data by their types.

from geopy import Point
import pandas as pd 
from ems.settings import Settings

class Data ():


    def __init__ (self, settings):
        assert isinstance (settings, Settings)

        self.traveltimes = self.file_to_traveltimes()
        self.cases = self.file_to_cases()
        self.bases = self.file_to_locations(settings.bases_file)
        self.demands = self.file_to_locations(settings.demands_file)
        self.clustered_demands = [] # TODO algorithm.init_bases() ?


    def file_to_locations (self, file):
        """
            Reads locations from CSV file which must have the first line labelled with
            latitude, longitude. See the Data as an example.
        """
        assert file is not None
        assert file is not ""
        assert isinstance (file, str)

        desired_info = ['latitude', 'longitude']

        raw = pd.read_csv (file)

        keys_read = raw.keys()

        for key in desired_info:
            if key not in keys_read:
                raise Exception("{} was not found in keys of file {}".format(key, file))
        
        return raw[desired_info]


    def file_to_cases (self):
        # TODO
        return


    def file_to_traveltimes (self):
        # TODO
        return



class Case ():
    def __init__ (self, x = None, y = None):
        if all ([x is None, y is None]): raise Exception ("Case: none of the parameters have objects. ")
        self.location = Point (x,y)


class Base ():
    def __init__ (self, x = None, y = None):
        if all ([x is None, y is None]): raise Exception ("Base: none of the parameters have objects. ")
        self.location = Point (x,y)


class Demand ():
    def __init__ (self, x = None, y = None):
        if all ([x is None, y is None]): raise Exception ("Demand: none of the parameters have objects. ")
        self.location = Point (x,y)


class TravelTime ():


    def __init__(self):
        pass


    def getTime (base, demand):
        pass
