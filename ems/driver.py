"""
Read the user arguments and configurations which will be created as Python objects
recursively in the Driver.
"""
import importlib

from ems.config_reader.loaders import UserArguments

def read_user_input():
    """ Sets up the command line interface to ask for config file location """
    # TODO If we don't want to support optional command line args,
    # TODO UserArgument's implementation can go here.

    usr_args = UserArguments()
    return usr_args.get_sim_args()


class Driver:
    """
    Use recursion to create objects as a tree of simulator objects with the simulator at the
    highest level and any subsequent objects a subitem.
    """
    def __init__(self, objects=None):
        if objects is None:
            objects = {}
        self.objects = objects

    # If key in d already exists in self.objects, overwrites it
    def create_objects(self, dictionary):

        # Parse objects and store
        for key, _ in dictionary.items():
            self.objects[key] = self.create(dictionary[key])

        # print(self.objects)

        # if "name" in self.objects:
            # print("Finished parsing: {}".format(self.objects["name"]))

    def create(self, obj):
        """
        For each item in the YAML file that has a classpath and classname, instantiate the
        respective module and class object. This method uses recursion to traverse the nested
        yaml file.

        :param obj: an object in the yaml file, could be a list, dict, or value (string or
        number)
        :return: the python object representation of the object
        """

        # Dictionary (nest object)
        if isinstance(obj, dict):
            params = {}
            cname = cpath = None
            for key, value in obj.items():
                # Parse into class and classname
                if key == "class":
                    cname_parts = value.split('.')
                    cname = cname_parts[-1]
                    cpath = '.'.join(cname_parts[:-1])

                # Parameter: recurse to create object for parameter
                else:
                    params[key] = self.create(value)

            # print("Instantiating: {}".format(cname)) # TODO Change to log
            class_constructor = getattr(importlib.import_module(cpath), cname)
            instance = class_constructor(**params)
            return instance

        # List of objects
        elif isinstance(obj, list):
            return [self.create(ele) for ele in obj]

        # If key pointing to existing object
        elif isinstance(obj, str) and obj[0] == "$":
            return self.objects[obj[1:]]

        # Primitive
        else:
            return obj
