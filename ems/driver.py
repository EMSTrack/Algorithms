from ems.config_reader.loaders import UserArguments
import importlib

def read_user_input():
    """ Sets up the command line interface to ask for config file location """
    # TODO If we don't want to support optional command line args, UserArgument's implementation can go here.

    usr_args = UserArguments()
    return usr_args.get_sim_args()

def instantiate_simulator(d):
    """
    For each item in the YAML file that has a classpath and classname, instantiate the
    respective module and class object. This method uses recursion to traverse the nested
    yaml file.

    :param d: an object in the yaml file, which could be a list, dict, or value (string or number)
    :return: the python object representation of the object
    """
    cname = cpath = None
    params = {}

    for key, value in d.items():
        # Class
        if key == "class":
            cname = value

        # Classpath
        elif key == "classpath":
            cpath = value

        # Nested object param
        elif isinstance(value, dict):
            params[key] = instantiate_simulator(value)

        # Nested list param
        elif isinstance(value, list):
            a = []
            for ele in value:
                if isinstance(ele, dict):
                    a.append(instantiate_simulator(ele))
                else:
                    a.append(ele)
            params[key] = a

        # Primitive param
        else:
            params[key] = value

    c = getattr(importlib.import_module(cpath), cname)
    instance = c(**params)
    return instance
