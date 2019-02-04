from ems.config_reader.loaders import UserArguments
import importlib

def read_user_input():
    """ Sets up the command line interface to ask for config file location """
    # TODO If we don't want to support optional command line args, UserArgument's implementation can go here.

    usr_args = UserArguments()
    return usr_args.get_sim_args()


class Driver:

    def __init__(self, objects=None):
        if objects is None:
            objects = {}
        self.objects = objects

    # If key in d already exists in self.objects, overwrites it
    def create_objects(self, d):

        # Parse objects and store
        for key, value in d.items():
            self.objects[key] = self.create(d[key])

        if "name" in self.objects:
            print("Finished parsing: {}".format(self.objects["name"]))

    def create(self, o):
        """
        For each item in the YAML file that has a classpath and classname, instantiate the
        respective module and class object. This method uses recursion to traverse the nested
        yaml file.

        :param o: an object in the yaml file, which could be a list, dict, or value (string or number)
        :return: the python object representation of the object
        """

        # Dictionary (nest object)
        if isinstance(o, dict):
            params = {}
            cname = cpath = None
            for key, value in o.items():
                # Class
                if key == "class":
                    cname = value

                # Classpath
                elif key == "classpath":
                    cpath = value

                # Parameter: recurse to create object for parameter
                else:
                    params[key] = self.create(value)

            print("Instantiating: {}".format(cname))
            c = getattr(importlib.import_module(cpath), cname)
            instance = c(**params)
            return instance

        # List of objects
        elif isinstance(o, list):
            return [self.create(ele) for ele in o]

        # If key pointing to existing object
        elif o in self.objects:
            return self.objects[o]

        # Primitive
        else:
            return o
