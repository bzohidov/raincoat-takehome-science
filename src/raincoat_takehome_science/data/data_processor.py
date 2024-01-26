#!/usr/bin/env python

import numpy as np
import geopandas as gpd
from shapely.geometry import Polygon
from geopy.distance import geodesic




def calculate_gradient_wind_speed_jelesnianski(r, rmax, vmax):
    """
    Calculates Jelesnianski (1965) formula for `Vg(r)` gradient wind speed
     at a distance of `r` from the center of typhoon/hurricane.

    Parameters:
      - r (float):    distance from the center of typhoon/hurricane, km.
      - vmax (float): maximum wind speed of typhoon/hurricane, knots.
      - rmax (float): radius of maximum wind (MW) of typhoon/hurricane, nmi.
    """
    if (0<=r) and (r<=rmax):
      vg = vmax * (r / rmax)**1.5
    elif r > rmax:
      vg = vmax * (rmax/r)**0.5
    else:
        vg = 0
    return vg


def filter_track_inside_area(trackdata, area):
  """
  Filters track data and returns the data that are only inside a given area with coordinates.

  Parameters:
    - trackdata  (DataFrame): Wind track data.
    - area  (dict):  Boundary coordinates of area (lat_max, lat_min, lon_max, lon_min).
  """

  # Create a Polygon representing the area of Puerto Rico
  area_puerto_rico = Polygon([(area['lon_min'], area['lat_min']),
                              (area['lon_max'], area['lat_min']),
                              (area['lon_max'], area['lat_max']),
                              (area['lon_min'], area['lat_max'])
                              ])

  # Create a GeoDataFrame from the DataFrame
  gdf = gpd.GeoDataFrame(trackdata, geometry=gpd.points_from_xy(trackdata['LONE/W'], trackdata['LATN/S']))

  # Filter data within the area of Puerto Rico
  gdf_within_area = gdf[gdf.geometry.within(area_puerto_rico)]

  return gdf_within_area


def calculate_distances(lat_array, lon_array, lat_point, lon_point):
  """
  Calculate the Haversine distance between an array of points and a single point
  given their latitude and longitude.
  
  Parameters:
  - lat_array, lon_array: Arrays of latitude and longitude for multiple points (in degrees)
  - lat_point, lon_point: Latitude and longitude of a single point (in degrees)
  
  Returns:
  - Array of distances between each point in the array and the single point (in kilometers)
  """
  coord_array = list(zip(lat_array, lon_array))
  coord_point = (lat_point, lon_point)
  return np.array([geodesic(coord, coord_point).meters for coord in coord_array])


def generate_swath_data(df, area, grid_resolution):
    """
    Generates a wind intensity swath based on the provided b-deck data in a given area.

    Parameters:
      #/      - lats (1D array): Latitude, degrees.
      #/      - lons (1D array): Longitude, degrees.
      #/      - vmax (1D array): Maximum wind speed, m/s.
      #/      - rmw (1D array): Radiues of maximum wind, meter.
      - df (DataFrame): Time series of wind speed data containing latitude, longitude, maximum wind speed and radius of maximum wind values.
      - area (dict): Geographic area of interest for swath. Usually, latitude max, min, and longitude max, min values.
      - grid_resolution (float): Grid resolution, 0.1 by default.

    Returns:
      - ndarray: Wind intensity swath.
    """
    print('Swath generation started....')

    data = df[['LATN/S', 'LONE/W', 'VMAX', 'RMW']].values
    lats, lons, vmax, rmw = data[:,0], data[:,1], data[:,2], data[:,3]

    # A grid over Puerto Rico
    grid_lat, grid_lon = np.meshgrid(np.arange(area['lat_min'], area['lat_max'] + grid_resolution, grid_resolution),
                                      np.arange(area['lon_min'], area['lon_max'] + grid_resolution, grid_resolution)
                                      )

    # Initialize array for max wind speed
    swath_of_max_wind_speed = np.zeros_like(grid_lat)

    # Calculate wind speed for each data point
    for lat, lon, vmax, rmax in zip(lats, lons, vmax, rmw):

        # Calculate distances from the current point to each grid point
        r_distances = calculate_distances(grid_lat.flatten(), grid_lon.flatten(), lat, lon)
        
        # Calculate the gradient wind speed for each grid point
        vg_values = np.vectorize(lambda r: calculate_gradient_wind_speed_jelesnianski(r, rmax, vmax))(r_distances.reshape(grid_lat.shape))
        
        # Update the swath_max_wind_speed array with the maximum values
        swath_of_max_wind_speed = np.maximum(swath_of_max_wind_speed, vg_values)
    
    print('Swath generation finished....')
    
    return swath_of_max_wind_speed, grid_lat, grid_lon