"""
Module for analyzing tag and beacon data
"""
import pandas as pd


def distance_overlap_check(positions: pd.DataFrame, tag_distance: pd.DataFrame):
    """
    Check the difference between (filtered) beacon distance data and tag distance data.
    :param positions: DataFrame containing beacon data.
    :param tag_distance: DataFrame containing tag data.
    :return: DataFrame with the difference in distances between beacon and tag data.
    """

    # Separate beacon data by tag id
    position_a = positions[positions['TagID'] == 'A'].copy()
    position_b = positions[positions['TagID'] == 'B'].copy()

    # Calculate distance based on beacon-tag data
    beacon_distance = pd.DataFrame({'x': position_a['x [m]'].values - position_b['x [m]'].values,
                                    'y': position_a['y[m]'].values - position_b['y[m]'].values})
    beacon_distance['distance'] = (beacon_distance['x'] ** 2 + beacon_distance['y'] ** 2) ** 0.5

    # Find difference in distance between beacon-tag data and tag-tag data
    difference = pd.DataFrame({'diff': beacon_distance['distance'].values - tag_distance['Distance [m]'].values})
    diff_mean = difference.mean()

    print(f'Average distance difference between (filtered) beacon data and tag data is {diff_mean.iloc[0]:.3f} m, which'
          f' is {(diff_mean.iloc[0] / 1.5 * 100):.1f}% of the defined 1.5 m contact distance. \n')

    # TODO
    # Hardcoded for 2 tags, but expand code to support varying amount of tags
    # Think of cut-off where difference between beacon and tag data is too large
    return difference


def contact_moments(positions: pd.DataFrame, tag_distance: pd.DataFrame, contact_distance: float = 1.5):
    """
    Find and analyze contact moments based on tag data.
    :param positions: DataFrame containing beacon data.
    :param tag_distance: DataFrame containing tag data.
    :param contact_distance: Distance threshold to define a contact moment (default is 1.5 m).
    :return: DataFrame containing contact data (time, distance),
             List of tuples representing start and end of contact moments (start index, end index).
    """

    # Construct copy of the data where contact occurred, and added position
    contact_data = tag_distance[tag_distance['Distance [m]'] <= contact_distance].copy()
    contact_data = contact_data.set_index('Time [s]')

    # Hardcoded for 'A' and 'B' tag IDs, develop more universal method to find id of used tag
    self_id = ''
    if tag_distance['ContactID'][0] == 'B':
        self_id = 'A'
    else:
        self_id = 'B'

    # Add x, y positions from beacon data
    contact_data['x'] = positions[positions['TagID'] == self_id].set_index('Time [s]')['x [m]']
    contact_data['y'] = positions[positions['TagID'] == self_id].set_index('Time [s]')['y[m]']

    # Most data can be derived from finding the indices where the distance falls beneath contact distance or conversely
    in_contact = False
    start_index = 0
    contact_indices = []

    for index, row in tag_distance.iterrows():
        if row['Distance [m]'] < contact_distance:
            if not in_contact:
                start_index = index
                in_contact = True
        else:
            if in_contact:
                end_index = index - 1
                contact_indices.append((start_index, end_index))
                in_contact = False

    # Check for case where tags are in contact until end of data array
    if in_contact:
        contact_indices.append((start_index, len(tag_distance) - 1))

    if self_id == 'A':
        print(f'For {len(contact_data) / 10} s out of {len(tag_distance) / 10} s, tags were in contact distance of each'
              f' other \n')
        print(f'In total {len(contact_indices)} contact moment(s) occurred, with an average duration of '
              f'{len(contact_data)/10/len(contact_indices)} s \n')

    # TODO
    # Think of more information that could be derived

    return contact_data, contact_indices


if __name__ == '__main__':
    pass
