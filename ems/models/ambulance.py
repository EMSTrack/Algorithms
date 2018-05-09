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

        self.id:int = id
        self.base:Base = base
        self.unit:str = unit
        self.deployed:bool = deployed
        self.location:Point = location
        self.deployed_time:datetime.datetime = deployed_time
        self.end_time:datetime.datetime = end_time

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

        # Raise exception if ambulance is not deployed
        if not self.deployed:
            raise Exception("Ambulance {} not yet deployed, cannot finish".format(self.id))

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

        # Raise exception if ambulance is already deployed
        if self.deployed:
            raise Exception("Ambulance {} already deployed".format(self.id))

        if not datetime:
            raise Exception("Cannot set a deployed ambulance's deploy time to None")

        if not end_time:
            raise Exception("Cannot set a deployed ambulance's end time to None")

        self.deployed = True
        self.deployed_time = datetime
        self.end_time = end_time
        self.location = destination
