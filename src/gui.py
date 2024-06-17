"""
Module with basic GUI function
"""

import PySimpleGUI as sg
import pandas as pd
import src.data_read as dr
import src.data_verification as dver
import src.data_processing as dp
import src.data_analysis as da
import src.data_visualization as dvis


def open_gui():
    # Define the layout of the GUI
    layout = [
        [sg.Text('Select files:')],
        [sg.Text('Beacon data:', size=(15, 1)), sg.InputText(key='-POSITIONS-'), sg.FileBrowse()],
        [sg.Text('Tag A data:', size=(15, 1)), sg.InputText(key='-TAGA-'), sg.FileBrowse()],
        [sg.Text('Tag B data:', size=(15, 1)), sg.InputText(key='-TAGB-'), sg.FileBrowse()],
        [sg.Button('Run analysis'), sg.Button('Run animation')],
        [sg.Output(size=(60, 20))]
    ]

    # Create the window
    window = sg.Window('Pathogen transfer estimate', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        elif event == 'Run analysis':
            # Read data from files
            file_positions = values['-POSITIONS-']
            file_tag_a = values['-TAGA-']
            file_tag_b = values['-TAGB-']

            try:
                positions = dr.read_position_data(file_positions)
                tag_a = dr.read_tag_data(file_tag_a)
                tag_b = dr.read_tag_data(file_tag_b)

                unique_tag_ids = ('A', 'B')

                try:
                    dver.check_tags(unique_tag_ids, positions)
                except ValueError:
                    missing_tag_ids = dver.find_missing_tags(unique_tag_ids, positions)
                    positions = dp.correct_tag_ids(unique_tag_ids, missing_tag_ids, positions)

                dp.remove_noise(unique_tag_ids, positions)

                # Perform data analysis
                da.distance_overlap_check(positions, tag_a)

                contact_data_a, _ = da.contact_moments(positions, tag_a)
                contact_data_b, _ = da.contact_moments(positions, tag_b)

                # Visualize processed data
                dvis.plot_contact_locations(contact_data_a, contact_data_b)

            except FileNotFoundError:
                print('Error: missing file locations.')

        elif event == 'Run animation':
            # Read data from file
            file_positions = values['-POSITIONS-']

            try:
                positions = dr.read_position_data(file_positions)

                unique_tag_ids = ('A', 'B')

                try:
                    dver.check_tags(unique_tag_ids, positions)
                except ValueError:
                    missing_tag_ids = dver.find_missing_tags(unique_tag_ids, positions)
                    positions = dp.correct_tag_ids(unique_tag_ids, missing_tag_ids, positions)

                dp.remove_noise(unique_tag_ids, positions)

                # Animate data
                dvis.animate(unique_tag_ids, positions)

            except FileNotFoundError:
                print('Error: missing file locations.')

    window.close()


if __name__ == '__main__':
    open_gui()
    pass
