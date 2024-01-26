#!/usr/bin/env python

import netCDF4 as nc
import os

def generate_nc(swath_max_wind_speed, grid_lon, grid_lat, timestamp, to_file):
    """
        Generates netCDF swath data to netCDF file.

    Parameters:
        - swath_max_wind_speed (ndarray): Wind intensity data.
        - grid_lat (ndarray): Latitude grid.
        - grid_lon (ndarray): Longitude grid.
        - area (list or tuple): Area in which data is plotted. 

    """

    with nc.Dataset(to_file, 'w', format='NETCDF4') as ncfile:
        ncfile.createDimension('lon', len(grid_lon[0]))
        ncfile.createDimension('lat', len(grid_lat))
        ncfile.createDimension('time', len(timestamp))

        lon_var = ncfile.createVariable('lon', 'f4', ('lon',))
        lat_var = ncfile.createVariable('lat', 'f4', ('lat',))
        t_var = ncfile.createVariable("time","f8",("time",))
        wind_speed_var = ncfile.createVariable('wind_speed', 'f4', ('time', 'lat', 'lon'))

        lon_var[:] = grid_lon[0]
        lat_var[:] = grid_lat[:, 0]
        t_var[:] = timestamp
        wind_speed_var[:, :] = swath_max_wind_speed

        print('Swath data {} file has been created in {}'.format(os.path.basename(to_file), to_file))

    return None
