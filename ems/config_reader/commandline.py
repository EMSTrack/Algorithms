import argparse

class SimulatorCLI:
    """ This class uses argparse to define how the user can see the simulator via the command line interface. """

    def __init__(self):
        """ Define the command line tool here. Use helper methods as needed. """
        parser = argparse.ArgumentParser(description="Load configurations, data, preprocess models. Run simulator on "
                                                     "ambulance dispatch. Decisions are made during the simulation, but "
                                                     "the events are output to a csv file for replay.")

        parser.add_argument('configurations',
                            help="The simulator needs a configuration to begin the computaiton.",
                            type=str,
                            )

        # TODO LAST: All the configurations that can be set in the configuration files should be override-able here.
        # parser.add_argument('--configurations',
        #                     help="for example, '--configurations hans'. Don't include '.json'",
        #                     type=str,
        #                     required=True)

        parser.add_argument('--ambulances',
                            help="Number of ambulances",
                            type=int,
                            required=False)

        parser.add_argument('--bases',
                            help='Number of bases',
                            type=int,
                            required=False)

        parser.add_argument('--slices',
                            help="Number of cases to simulate",
                            type=int,
                            required=False)

        parser.add_argument('--output-file',
                            help="Output filename for simulator info",
                            type=str,
                            required=False)

        parser.add_argument('--debug',
                            help="Whether the simulator should run in debug-mode.",
                            type=bool,
                            required=False,
                            default=True)

        self.parser = parser

    def args(self):
        return self.parser.parse_args()