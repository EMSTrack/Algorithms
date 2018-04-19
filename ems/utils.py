import pandas as pd 
from operator import itemgetter

def parse_headered_csv (file, desired_keys):

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


def parse_unheadered_csv (file, positions, header_names):

    assert file is not None
    assert positions is not None
    assert all(isinstance(ele, int) for ele in positions)
    assert header_names is not None
    assert all(isinstance(ele, str) for ele in header_names)
    assert len(positions) == len(header_names)

    raw = pd.read_csv (file)
    headered_df = pd.DataFrame()

    for pos, header in zip(positions, header_names):
        headered_df[header] = raw.iloc[:, pos]

    return headered_df

