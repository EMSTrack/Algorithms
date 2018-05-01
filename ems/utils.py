import pandas as pd


def parse_headered_csv (file: str, desired_keys: list):
    """
    Takes a headered CSV file and extracts the columns with the desired keys
    :param file: CSV filename
    :param desired_keys: Names of columns to extract
    :return: pandas dataframe
    """

    if file is None:
        return None

    raw = pd.read_csv (file)

    keys_read = raw.keys()

    for key in desired_keys:
        if key not in keys_read:
            raise Exception("{} was not found in keys of file {}".format(key, file))

    return raw[desired_keys]


def parse_unheadered_csv (file: str, positions: list, header_names: list):

    """
    Takes an unheadered CSV file, extracts the columns based on given positions,
    and provides them headers for the pandas dataframe
    :param file: CSV filename
    :param positions: Indices of the columns to extract
    :param header_names: Header names for the extracted columns
    :return: pandas dataframe
    """

    if file is None:
        return None

    raw = pd.read_csv (file)
    headered_df = pd.DataFrame()

    for pos, header in zip(positions, header_names):
        headered_df[header] = raw.iloc[:, pos]

    return headered_df

