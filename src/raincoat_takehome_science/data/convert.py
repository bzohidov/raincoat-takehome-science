#!/usr/bin/env python


from pandas import to_datetime
import pyproj as proj


def convert_latlon_hemi_2_degree(lat_str, lon_str):
    """
    Converts latitude and longitude data hemispheric format into degree format.
    
    Parameters:
        - lat_str (str): latitude.
        - lon_str (str): longitude.

    Returns:
        - lat_degrees (float)
        - lon_degrees (float)
    """
    # Extract numerical values and hemisphere indicators
    lat_value, lat_hem = float(lat_str[:-1])/10., lat_str[-1]
    lon_value, lon_hem = float(lon_str[:-1])/10., lon_str[-1]

    # Adjust sign based on hemisphere indicators
    lat_degrees = lat_value if lat_hem.upper() == 'N' else -lat_value
    lon_degrees = lon_value if lon_hem.upper() == 'E' else -lon_value

    return lat_degrees, lon_degrees


def speed_knots_2_ms(data):
    """
    Converts windspeed unit in knot [knt] into meter per second [ms] unit.

    Parameters:
        - data (float): Wind speed in knots.
    """
    return data*0.51444


def nautical_miles_2_meter(data):
    """
    Converts distance in nautical miles [nmi] into meter [m] unit.

    Parameters:
        - data (float): Nautical miles, [nmi].
    """
    return data * 1852.0


def timestamp_str_2_datetime(time):
    """
    Converts string formatted timestamp into pandas datetime format.

    Parameters:
        - time (str or Series): Timestamp in yyyymmddhh (year, month, day, hour) order. Example, 20171230
    """
    return to_datetime(time, format='%Y%m%d%H')


def latlon_2_xy(lat, lon):
    """
    Convert latitude and longitude to Cartesian coordinates.

    Parameters:
    - lat (1D array): Latitude in degrees
    - lon (1D array): Longitude in degrees

    Returns:
    - x, y: Cartesian coordinates
    """
    # Puerto Rico zone 20
    p = proj.Proj(proj='utm',zone=20,ellps='WGS84', preserve_units=False)

    return p(lon, lat)