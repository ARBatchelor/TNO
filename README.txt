# TNO spreading of pathogens case

## Introduction
This repository contains a Python application designed to analyze and visualize beacon and tag data obtained from sensor measurements in a controlled environment. The tool processes CSV files containing position data and tag interactions, verifies data integrity, performs analysis to determine contact moments, visualizes contact locations, and animates tag movements over time.
Developed in Python v3.10

## Installation
Make sure PySimpleGUI is installed, more information can be found [here](https://pysimplegui.com/).  
Clone the repository

To run the application, execute `main.py`

## GUI Usage
Upon launching `main.py`, a GUI window will appear.
Select the CSV files containing position data (`position.csv`), and tag data for Tag A (`TagA.csv`) and Tag B (`TagB.csv`).
Click on "Run analysis" to initiate data analysis or "Run animation" to run the animation.
The application will process the data, perform analysis, and output some information in the terminal below.

## Modules

### `data_read.py`
Module to read CSV files containing tag and position data into pandas DataFrames.

### `data_verification.py`
Module to verify tag and position data integrity and correctness.

### `data_processing.py`
Module to preprocess and clean tag and position data, including correcting tag IDs and removing noise.

### `data_analysis.py`
Module to perform analysis on tag data, including calculating distances and identifying contact moments.

### `data_visualization.py`
Module to visualize tag data, including animating tag movements over time and plotting contact locations.

### `gui.py`
Module implementing a simple GUI using PySimpleGUI to interact with the data analysis and visualization functionalities.