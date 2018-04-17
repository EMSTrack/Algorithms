from geopy import Point

class Data ():

    def __init__ (self):
        self.traveltimes = []
        self.cases = []
        self.bases = []
        self.demands = []
        self.clustered_demands = []


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


def testCases ():
    print("Case 1: x, y ")
    case = Case (x=2, y=3)

    from IPython import embed; embed()


if __name__ == "__main__":
    testCases ()

