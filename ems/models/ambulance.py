import datetime

from geopy import Point

from ems.models.base import Base


# Define the Ambulance model.

class Ambulance:

    def __init__(self,
                 id: int,
                 base: Base,
                 unit: str = "XXX-XXXX",
                 deployed: bool = False,
                 location: Point = None,
                 deployed_time: datetime.datetime = None,
                 end_time: datetime.datetime = None):

        self.id = id
        self.base = base
        self.unit = unit
        self.deployed = deployed
        self.location = location
        self.deployed_time = deployed_time
        self.end_time = end_time

    def __eq__(self, other):
        """
        Checks for equality
        :return: True if objects are equal; else False
        """

        if type(other) is Ambulance and self.id == other.id:
            return True

        return False

    def finish(self):
        """
        Resets the ambulance.
        :return: None. This just changes state.
        """

        # TODO raise exception if ambulance is not deployed?

        self.deployed = False
        self.location = None
        self.deployed_time = None

    def deploy(self, datetime, destination, end_time):
        """
        Deploys the ambulance by setting the deployed state, start times, end time, and location.
        :param datetime:
        :param destination:
        :param end_time: 
        :return: Nothing. This function only changes state.
        """

        if self.deployed: raise Exception("Ambulance {} already deployed".format(self.id))

        self.deployed = True
        self.deployed_time = datetime
        self.end_time = end_time
        self.location = destination

        if not datetime:
            raise Exception("Cannot set a deployed ambulance's deploy time as None")
