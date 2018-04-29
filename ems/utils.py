# Maybe move back into dataset file;

import geopy
import geopy.distance
import numpy as np
import pandas as pd


def closest_distance(list_type, target_point):
    """
    Finds the closest point in the corresponding generic list.
    For example, find the closest base given a GPS location.
    :param list_type:
    :param target_point:
    :return: the position in that list
    """

    # Compute differences between target point and each element's location in list type
    differences = [geopy.distance.vincenty(target_point, element.location).km for element in list_type]

    # Find the index of the minimum difference and return the element at that index
    min_index = np.argmin(differences)
    return list_type[min_index]


    # for index in range(len(list_type)):
    #     # print(list_type)
    #     if list_type[index] is not None:
    #
    #         difference = geopy.distance.vincenty(target_point, list_type[index].location).km
    #         if shortest_difference > difference:
    #             shortest_difference = difference
    #             position = index
    #             # print (type(difference), shortest_difference)
    #             if shortest_difference < 0.5:
    #                 return list_type[position]

    # return list_type[position]


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

