"""
Module for reading tag- and position-data files into pandas Dataframes for further analysis and usage.
Could be expanded upon when files other than .csv are added in future usage.
"""
import pandas as pd


def read_tag_data(tag_file: str) -> pd.DataFrame:
    """
    Read tag data from a CSV file into a pandas DataFrame.
    :param tag_file: File path to the CSV file containing tag data
    :return tag_data: DataFrame containing the tag data
    """
    tag_data = pd.read_csv(tag_file)
    return tag_data


def read_position_data(positions_file: str) -> pd.DataFrame:
    """
    Read beacon data from a CSV file into a pandas DataFrame.
    :param positions_file: File path to the CSV file containing beacon data.
    :return: DataFrame containing the beacon data
    """
    positions = pd.read_csv(positions_file)
    return positions


if __name__ == '__main__':
    pass
