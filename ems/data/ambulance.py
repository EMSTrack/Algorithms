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

        self.id                 = None
        self.unit               = "XXX-XXXX"
        self.deployed           = False
        self.base               = None
        self.location           = None
        self.deployed_time      = None
        self.end_time           = None


    def finish(self, current_datetime):
        """
        Resets the ambulance.
        :return: None. This just changes state.
        """

        # TODO raise exception if ambulance is not deployed?

        self.deployed       = False
        self.location       = None
        self.deployed_time  = None

        if debug: print(f'{Fore.CYAN}Retiring ambulance ', self.id, 'at time', current_datetime,
                    f"{Style.RESET_ALL}")


    def deploy(self, datetime, destination, ambulance_delta):
        """
        Deploys the ambulance by setting the deployed state, start times, end time, and location.
        :param datetime:
        :param destination:
        :param ambulance_delta:
        :return: Nothing. This function only changes state.
        """
        if debug: print(f"{Fore.GREEN}Deploying ambulance", self.id, 'at time', datetime, f'{Style.RESET_ALL}')

        if ambulance.deployed: raise Exception("Ambulance {} already deployed".format(self.id))

        self.deployed           = True
        self.deployed_time      = datetime
        self.end_time           = datetime + ambulance_delta
        self.location           = destination

        if not datetime:
            raise Exception("Cannot set a deployed ambulance's deploy time as None")
