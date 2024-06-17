"""
Module for visualizing beacon and tag data, and derived contact moments.
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def animate(unique_tag_ids: tuple, positions: pd.DataFrame, room_dimensions: tuple = (0, 10, 0, 10)):
    """
    Generate an animation of tagged persons' movement in a room over time.
    :param unique_tag_ids: Tuple of unique tag IDs.
    :param positions: DataFrame containing beacon data.
    :param room_dimensions: Tuple of 2D room dimensions ((xmin, xmax, ymin, ymax), default is (0, 10, 0, 10))
    :return:
    """

    fig, ax = plt.subplots()

    scatter_a = ax.scatter(positions[positions['TagID'] == 'A']['x [m]'][0],
                           positions[positions['TagID'] == 'A']['y[m]'][0], label='A')
    scatter_b = ax.scatter(positions[positions['TagID'] == 'B']['x [m]'][1],
                           positions[positions['TagID'] == 'B']['y[m]'][1], label='B')

    # Set axis limits to 2D room dimensions, with corner (0,0) bottom left
    ax.set_xlim(room_dimensions[0], room_dimensions[1])
    ax.set_ylim(room_dimensions[2], room_dimensions[3])
    plt.legend()
    plt.title("Tagged persons' movement over time in room")

    def update(frame):
        # Prevent looping of animation by closing figure when final frame is reached
        if frame == num_of_frames - 1:
            plt.close()

        # Update data for new frame
        current_data_a = positions.iloc[frame * len(unique_tag_ids)]
        scatter_a.set_offsets(current_data_a[['x [m]', 'y[m]']])
        current_data_b = positions.iloc[frame * len(unique_tag_ids) + 1]
        scatter_b.set_offsets(current_data_b[['x [m]', 'y[m]']])

        return scatter_a, scatter_b

    # Optional TODO:
    # - Add a visual indicator of 1.5 m contact distance from person, change color when in contact with other person
    # - Find more universal way to deal with plotting differing amount of tags

    num_of_frames = int(len(positions) / len(unique_tag_ids))
    ani = FuncAnimation(fig, update, frames=num_of_frames, blit=True, interval=20)

    plt.show()
    return


def plot_contact_locations(contact_data_a: pd.DataFrame, contact_data_b: pd.DataFrame,
                           room_dimensions: tuple = (0, 10, 0, 10)):
    """
    Plot the locations of contact moments between tagged persons.
    :param contact_data_a: DataFrame containing contact moment data for tag A.
    :param contact_data_b: DataFrame containing contact moment data for tag B.
    :return:
    """
    fig, ax = plt.subplots()
    scatter_a = ax.scatter(contact_data_a['x'], contact_data_a['y'], label='Tag A contact locations')
    scatter_b = ax.scatter(contact_data_b['x'], contact_data_b['y'], label='Tag B contact locations')
    ax.set_xlim(room_dimensions[0], room_dimensions[1])
    ax.set_ylim(room_dimensions[2], room_dimensions[3])
    plt.title('Location of contact between tagged persons')
    plt.legend()
    plt.show()

    # TODO
    # Hardcoded for 2 tags, develop more universal way to deal with x amount of tags
    return


# def plot_contact_moments():
#     # Statistical plots of contact moments for person X (e.g. amount of contact moments, avg time, standard dev.)
#     # For case data of only 1 person should be fine (since the other person by default has the same statistics),
#     # however in future use it is probable that statistics of more than one person will be required
#     return


if __name__ == '__main__':
    pass
