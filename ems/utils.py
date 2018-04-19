import pandas as pd 

def parse_csv (file, desired_keys):

    assert file is not None
    assert file is not ""
    assert isinstance (file, str)
    assert isinstance (desired_keys, list)
    assert all(isinstance(ele, str) for ele in desired_keys)

    raw = pd.read_csv (file)

    keys_read = raw.keys()

    for key in desired_keys:
        if key not in keys_read:
            raise Exception("{} was not found in keys of file {}".format(key, file))

    return raw[desired_keys]