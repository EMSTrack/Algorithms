from ems.config_reader.commandline import SimulatorCLI
from ems.config_reader.reader import ResolveConfigs

# TODO: Goal of this file is to abstract out a lot of the run.py in the above directory.
# TODO: user inputs from CLI args (parse_args) and configurations stored in the files.

class UserInput: # TODO Request for comments (RFC) on name
    """ Returns the configuration as the initial condition. The CLI overrides the config files."""
    # do parse_arg stuff here

    def __init__(self):
        """

        """
        command_line_args = SimulatorCLI().args()
        settings = ResolveConfigs(debug=command_line_args.debug, args=command_line_args)
        self.args = settings

    # do read files for stored data here. command line should always override files
    # YAML reduces syntax hell



# TODO: pre-simulator computation setup like kd-trees and polygon
    # TODO Or should the polygon computation be in another folder?
class SetupPrecondition:
    """  """
    pass


# TODO: Simulator
class SimulatorRunner:
    """  """
    pass

