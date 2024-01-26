#!/usr/bin/env python

import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.raincoat_takehome_science.data.reader_bdeck import generate_intermediate_data
from src.raincoat_takehome_science.data.data_processor import generate_swath_data
from src.raincoat_takehome_science.plotting.swath_plotter import plot_swath_wind_speed
from src.raincoat_takehome_science.data.save_to_netcdf import generate_nc


import click
from config import config

@click.command()
@click.option('--input_file', type=click.Path(exists=True), default='data/external/bal152017.dat', help='Path to the input file.')
@click.option('--config_file', type=click.Path(exists=True),  default='config/config.yaml', help='Path to the YAML configuration file.')
def run(input_file, config_file):
    """
    Process input file and save the output.

    Parameters:
    - input_file (str): Path to the input file.
    - config_file (str): Path to the YAML configuration file.
    """
    try:
        # Read configuration parameters
        params = config.read_config(config_file)
            
        # Load data from the b-deck file as dataframe
    #    df1 = load_b_deck_file(input_file)

        # Convert parameters units and Generate the converted data
        df2 = generate_intermediate_data(input_file,
                                        params['files']['path_bdeck_intermediate']
                                        )

        # Choose area of interest from the data
        #df_filtered = filter_track_inside_area(df_converted)

        # DELIVERIES:
        # 1. Generate swath data

        swath_max_wind_speed, grid_lat, grid_lon = generate_swath_data(df2,
                                                                    params['area'],
                                                                    params['grid_resolution']
                                                                    )

        # 2. Generate netcdf and save it
        generate_nc(swath_max_wind_speed,
                    grid_lon,
                    grid_lat,
                    df2['YYYYMMDDHH'].values,
                    params['files']['output_ncfile']
                    )

        # 3. Plot the wind intensity map
        plot_swath_wind_speed(swath_max_wind_speed, 
                            grid_lon,
                            grid_lat,
                            [-68., -65., 17., 19.],
                            params['files']['output_plot_swath_wind_speed'],
                            params['plotting']['showfig']
                            )

        click.echo("Processing complete. Outputs saved to: {} and {}".format(params['files']['output_plot_swath_wind_speed'], params['files']['output_ncfile']))
    except Exception as e:
        click.echo(f"Error processing file: {str(e)}")

if __name__=='__main__':
    run()