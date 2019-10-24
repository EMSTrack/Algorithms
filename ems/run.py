import importlib
import yaml


class Driver:

    def __init__(self, yamlfile='', **kwargs):
        if yamlfile:
            kwargs.update(yaml.full_load(open(yamlfile, 'r')))
        self.params = kwargs

    def create_simulator(self):
        data = Driver._create_objects(self.params)
        sim = data.pop('simulator')
        return sim, data

    # If key in d already exists in self.objects, overwrites it
    @staticmethod
    def _create_objects(params):

        # Parse objects and store
        objects = {}
        for key, value in params.items():
            objects[key] = Driver._create_recurse(value, objects)

        return objects

    @staticmethod
    def _create_recurse(param, objects):
        """
        For each item in the YAML file that has a classpath and classname, instantiate the
        respective module and class object. This method uses recursion to traverse the nested
        yaml file.

        :param param: an object in the yaml file, which could be a list, dict, or value (string or number)
        :return: the python object representation of the object
        """

        # Dictionary (nest object)
        if isinstance(param, dict):
            params = {}
            cname = cpath = None
            for key, value in param.items():
                # Parse into class and classname
                if key == "class":
                    cname_parts = value.split('.')
                    cname = cname_parts[-1]
                    cpath = '.'.join(cname_parts[:-1])

                # Parameter: recurse to create object for parameter
                else:
                    params[key] = Driver._create_recurse(value, objects)

            # print("Instantiating: {}".format(cname)) # TODO Change to log
            c = getattr(importlib.import_module(cpath), cname)
            instance = c(**params)
            return instance

        # List of objects
        elif isinstance(param, list):
            return [Driver._create_recurse(ele, objects) for ele in param]

        # If key pointing to existing object
        elif isinstance(param, str) and param[0] == "$":
            return objects[param[1:]]

        # Primitive
        else:
            return param


if __name__ == "main":

    import argparse

    parser = argparse.ArgumentParser(
        description="Load configurations, data, preprocess models. Run simulator on "
                    "ambulance dispatch. Decisions are made during the simulation, but "
                    "the events are output to a csv file for replay.")

    parser.add_argument('config_file',
                        help="The simulator needs a configuration to begin the computation.",
                        type=str,)

    parser.add_argument('output_dir',
                        help="The simulator needs a configuration to begin the computation.",
                        type=str,
                        default=".")

    # parse arguments
    args = parser.parse_args()

    # create simulator
    driver = Driver(args.config_file)
    sim, data = driver.create_simulator()

    # run simulator
    case_record_set, metric_aggregator = sim.run()

    # Save the finished simulator information
    case_record_set.write_to_file(args.output_dir + '/processed_cases.csv')
    metric_aggregator.write_to_file(args.output_dir + '/metrics.csv')
