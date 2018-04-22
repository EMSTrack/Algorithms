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

        # TODO -- ambulance not deployed?
        # if not self.deployed:
        #     raise Exception?

        self.deployed       = False
        self.location       = None
        self.deployed_time  = None

        if debug: print(f'{Fore.CYAN}Retiring ambulance ', self.id, 'at time', current_datetime,
                    f"{Style.RESET_ALL}")
