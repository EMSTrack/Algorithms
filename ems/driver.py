from ems.config_reader.loaders import UserArguments
import importlib

# TODO: Goal of this file is to abstract out a lot of the run.py in the above directory.
# TODO: user inputs from CLI args (parse_args) and configurations stored in the files.

def read_user_input():
    usr_args = UserArguments()
    return usr_args.get_sim_args()

def instantiate_simulator(d):
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
