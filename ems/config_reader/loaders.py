import argparse
import yaml


class UserArguments:
    """
    This class reads the arguments from the user from two sources of truth:
        1) the command line
        2) the config file

    Then it will self resolve discrepancies.

    """

    def __init__(self):
        """ Define the command line tool here. Use helper methods as needed. """

        cli_args = self._command_line_args()
        file_contents = yaml.full_load(open(cli_args.config_file, 'r'))
        self.sim_args = file_contents

    def get_sim_args(self):
        return self.sim_args

    def _command_line_args(self):

        parser = argparse.ArgumentParser(
            description="Load configurations, data, preprocess models. Run simulator on "
                        "ambulance dispatch. Decisions are made during the simulation, but "
                        "the events are output to a csv file for replay.")

        parser.add_argument('config_file',
                                 help="The simulator needs a configuration to begin the computation.",
                                 type=str,
                                 # nargs='*'
                                 )

        return parser.parse_args()
