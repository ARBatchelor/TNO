"""
Module for verifying tag and beacon data integrity before further usage.
"""
import pandas as pd


def check_tags(unique_tag_ids: tuple, positions: pd.DataFrame):
    """
    Check if all specified tag IDs are present in the beacon data.
    Raises ValueError if any tag ID from unique_tag_ids is missing in the beacon data.
    :param unique_tag_ids: Tuple of unique tag IDs to be checked.
    :param positions: DataFrame containing the beacon data.
    :return:
    """

    for tag_id in unique_tag_ids:
        if tag_id not in positions['TagID']:
            raise ValueError(f'Tag {tag_id} ID missing in positions data')

    print('No missing tag IDs')

    return


def find_missing_tags(unique_tag_ids: tuple, positions: pd.DataFrame):
    """
    Identifies and returns which tag IDs from unique_tag_ids are missing in beacon data.
    :param unique_tag_ids: Tuple of unique tag IDs to be checked.
    :param positions: DataFrame containing the beacon data.
    :return: Tuple of missing tag IDs.
    """

    # identify which tag ids are present in beacon data
    existing_tag_ids = positions['TagID'].unique()

    missing_tag_ids = tuple([tag_id for tag_id in unique_tag_ids if tag_id not in existing_tag_ids])

    return missing_tag_ids


# def check_signal_noise(positions: pd.DataFrame):
#     # Write conditions to check if location data is too noisy, could be basis for automated filter settings
#     return
