"""
Module for processing tag and position data before analysis
"""

import pandas as pd


def correct_tag_ids(unique_tag_ids: tuple, missing_tag_ids: tuple, positions: pd.DataFrame) -> pd.DataFrame:
    """
    Function to correct tag-id error in the specific case where a singular tag-id is applied to beacon data. Assumes
    the beacon position.csv file lists data in alphabetical order of tag-id for each timestep. Also assumes no gaps
    between tag_id (i.e. when data from tag A and C is in the file, data from tag B is also present).
    :param unique_tag_ids: Tuple of unique tag IDs that should be present.
    :param missing_tag_ids: Tuple of missing tag IDs that need to be corrected.
    :param positions: DataFrame containing the beacon data.
    :return: Updated DataFrame with corrected tag IDs.
    """

    for tag_id in missing_tag_ids:
        indexes_to_change = []

        # Change ID character to integer value to find indices
        start_index = ord(tag_id.upper()) - 65

        indexes_to_change.extend(range(start_index, len(positions), len(unique_tag_ids)))

        # Change tag_id to correct one at calculated indices
        positions.loc[indexes_to_change, 'TagID'] = tag_id

    return positions


def remove_noise(unique_tag_ids: tuple, positions: pd.DataFrame):
    """
    Dampen noise in beacon data using a moving average filter.
    :param unique_tag_ids: Tuple of unique tag IDs.
    :param positions: DataFrame containing the position data.
    :return:
    """

    # Window size hardcoded, could be automated in future updates
    window_size = 10

    for tag in unique_tag_ids:

        # Copy isolated data of tag in question to apply filter on
        tag_data = positions[positions['TagID'] == tag].copy()

        # Apply moving average filter to x and y data
        filtered_x = pd.DataFrame(tag_data['x [m]'].rolling(window=window_size).mean())
        filtered_y = pd.DataFrame(tag_data['y[m]'].rolling(window=window_size).mean())

        # Replace NaN values with unfiltered values (based on right aligned window)
        filtered_x.iloc[0:window_size - 1, 0] = positions.loc[positions['TagID'] == tag, 'x [m]'][0:window_size - 1]
        filtered_y.iloc[0:window_size - 1, 0] = positions.loc[positions['TagID'] == tag, 'y[m]'][0:window_size - 1]

        # Substitute filtered data back into original dataframe
        positions.loc[positions['TagID'] == tag, 'x [m]'] = filtered_x[filtered_x['x [m]'].notnull()]
        positions.loc[positions['TagID'] == tag, 'y[m]'] = filtered_y[filtered_y['y[m]'].notnull()]

    # TODO:
    # Expand function/develop new function to support filtering tag-tag data
    # Use increasing window size to filter first values in data array
    return


# def interpolate_missing_values():
#     # Functionality to replace missing values, such as interpolation
#     return


if __name__ == '__main__':
    pass
