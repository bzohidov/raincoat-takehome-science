# Wind Intensity Calculation Solution

## Introduction
The project aims to generate a swath depicting the wind intensity over the island of Puerto Rico based
on the hurricane track provided by NOAA’s National Hurricane Center (NHC) in the form of a b-deck file.
The project is organized following the suggested structure, with modules for data reading, processing, plotting, CLI, and configuration.

In this coding solution, I used the formula originated by Jelesnianski (1965) formula for V(r), where V(r) is the maximum wind speed at a distance of r.

## Code Structure
To achieve that, the solution is divided into several sub-functions forming the following structure:

project_root/
│
├── data/
│   ├── external/
│   ├── interim/
│   └── processed/
│
├── cli/
│   ├── __init__.py
│   ├── bdeck_cli.py
│   ├── config_parser.py
│   └── main.py
│
├── docs/
│   └── SOLUTION.md
│
├── notebooks/
│   └── wind_speed_derivation.ipynb
│
├── output/
│
├── src/
│   ├── __init__.py
│   ├── data_processor.py
│   ├── bdeck_reader.py
│   └── swath_plotter.py
│
├── .gitignore
├── requirements.txt
└── README.md

The hurricane track is provided by NOAA’s National Hurricane Center (NHC) in the form of a b-deck file.

## Dependencies
- pandas (>= 1.5.3)
- numpy (>= 1.23.5)
- matplotlib (>= 3.7.1)
- cartopy (>= 0.22.0)

## Functionality
- `bdeck_reader`: Reads b-deck files into a DataFrame.
- `data_processor`: Implements wind speed calculation and swath generation.
- `swath_plotter`: Plots the generated swath using Cartopy.
- `bdeck_cli`: Command Line Interface for executing tasks.
- `config_parser`: Reads configuration from a YAML file.

## Configuration
Describes how to use the configuration file to customize the execution parameters.

## Example Usage
Provides examples of how to run the CLI with different configurations.

## Future Improvements
A room for enhancements or improvements towards the solution.
