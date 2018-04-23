from colorama import Fore
from colorama import Style

# Define the Ambulance model. 

class Ambulance():
    def __init__(self, 
                id, 
                base, 
                unit="XXX-XXXX",
                deployed=False,
                location=None,
                deployed_time=None,
                end_time=None):

        # TODO tyoe checking

        self.id                 = id
        self.base               = base
        self.unit               = unit
        self.deployed           = deployed
        self.location           = location
        self.deployed_time      = deployed_time
        self.end_time           = end_time

    def __eq__(self, other):

        if self.id == other.id:
            return True

        return False


    def finish(self, current_datetime):
        """
        Resets the ambulance.
        :return: None. This just changes state.
        """

        # TODO raise exception if ambulance is not deployed?

        self.deployed       = False
        self.location       = None
        self.deployed_time  = None


    def deploy(self, datetime, destination, ambulance_delta):
        """
        Deploys the ambulance by setting the deployed state, start times, end time, and location.
        :param datetime:
        :param destination:
        :param ambulance_delta:
        :return: Nothing. This function only changes state.
        """

        if self.deployed: raise Exception("Ambulance {} already deployed".format(self.id))

        self.deployed           = True
        self.deployed_time      = datetime
        self.end_time           = datetime + ambulance_delta
        self.location           = destination

        if not datetime:
            raise Exception("Cannot set a deployed ambulance's deploy time as None")
