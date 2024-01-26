# Wind Intensity Calculation Solution

## Introduction
The project aims to generate a swath depicting the wind intensity over the island of Puerto Rico based
on the hurricane track provided by NOAA’s National Hurricane Center (NHC) in the form of a b-deck file.
The project is organized following the suggested structure, with modules for data reading, processing, plotting, CLI, and configuration.

In this coding solution, I used the formula originated by Jelesnianski (1965) formula for V(r), where V(r) is the maximum wind speed at a distance of r.

## Code Structure
To achieve that, the solution is divided into several sub-functions forming the following structure:

|   CHANGELOG.md
|   pyproject.toml
|   README.md
|   requirements.txt
|   RESULTS.md
|   setup.cfg
|   setup.py
|   SOLUTION.md
|   structure.txt
|
|       
+---config
|       config.py
|       config.yaml
|       __init__.py
|       
+---data
|   |   
|   +---external
|   |       bal152017.dat
|   |       
|   +---interim
|   |       bal152017.dat
|   |       
|   \---processed
+---docs
|       quick_start.md
|       
+---notebooks
|       .gitkeep
|       
+---output
|       .gitkeep
|       
+---scripts
|       bdeck_cli.py
|       __init__.py
|       
\---src
    \---raincoat_takehome_science
        |   __init__.py
        |   
        +---data
        |       convert.py
        |       data_processor.py
        |       reader_bdeck.py
        |       save_to_netcdf.py
        |       __init__.py
        |       
        \---plotting
                swath_plotter.py
                __init__.py


The hurricane track is provided by NOAA’s National Hurricane Center (NHC) in the form of a b-deck file.

## Dependencies
- pandas (>= 1.5.3)
- numpy (>= 1.23.5)
- matplotlib (>= 3.7.1)
- cartopy (>= 0.22.0)
- xarray (>= 2023.7.0)
- yaml (>= 6.0.1)
- argparse (>= 1.1)
- netCDF4 (>= 1.6.5)


## Configuration
Describes how to use the configuration file to customize the execution parameters.

## Example Usage
Provides examples of how to run the CLI with different configurations.

## Future Improvements
A room for enhancements or improvements towards the solution.
