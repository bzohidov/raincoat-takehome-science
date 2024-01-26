#!/usr/bin/env python

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import numpy as np



def plot_swath_wind_speed(swath_max_wind_speed, grid_lon, grid_lat, area, path_to_save, showfig):
    """
    Plots the wind intensity swath over Puerto Rico using Cartopy.

    Parameters:
        - swath_max_wind_speed (ndarray): Wind intensity data.
        - grid_lat (ndarray): Latitude grid.
        - grid_lon (ndarray): Longitude grid.
        - area (list or tuple): Area in which data is plotted. 
        - path_to_save (str):   Path to save figure.
        - showfig (bool): Show figure or not.
    """

    # Implementation to plot swath using Cartopy
    fig, ax = plt.subplots(figsize=(10,6), subplot_kw = {'projection':ccrs.PlateCarree()})

    # Area to plot
    ax.set_extent(area)

    # Plot wind speed swath
    cf = ax.contourf(grid_lon, 
                     grid_lat, 
                     swath_max_wind_speed, 
                     cmap = plt.get_cmap('jet'), 
                     levels = np.linspace(0, np.around(np.max(swath_max_wind_speed)), 50), 
                     transform = ccrs.PlateCarree(),
                     extend='max'
                )
    # Add grid lines
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linestyle='--', linewidth=0.5, color='grey')
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    ax.set_title("Swath of Maximum Wind Speed over Puerto Rico")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    # Add coastlines and political boundaries for better context
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    
    # Add colorbar
    cbar = plt.colorbar(cf, ax=ax, orientation='vertical', fraction=0.04, pad=0.1, label='Wind Speed (m/s)')
    ax.set_title('Swath of Wind Speed over Puerto Rico')

    if path_to_save != '':
        fig.savefig(path_to_save)
        print('Plotted swath of wind speed has been saved in {}'.format(path_to_save))
    else:
        print("Plotted swath of wind speed has not been saved. The reason: input argument `path_to_save` has not been given.")
    
    if showfig:
        plt.show()


def plot_wind_center_locations(lats, lons, area=[-70, -60, 15, 20]):
    """
    Plots the wind intensity swath over Puerto Rico using Cartopy.

    Parameters:
    - swath_max_wind_speed (ndarray): Wind intensity data.
    - grid_lat (ndarray): Latitude grid.
    - grid_lon (ndarray): Longitude grid.
    """

    # Plotting
    fig, ax = plt.subplots(figsize=(10,6), subplot_kw={'projection': ccrs.PlateCarree()})
    ax.set_extent(area, crs=ccrs.PlateCarree())
    #lats, lons = data["LATN/S"].values, data["LONE/W"].values

    # Plot the point with a circle
    for lat, lon in zip(lats, lons):
        pnt, = ax.plot(lon, lat, 'ro', markersize=5, transform=ccrs.PlateCarree())
        #ax.add_patch(plt.Circle((lon, lat), 0.5, color='red', alpha=0.2, transform=projection))
    pnt.set_label('Wind center location')
    ax.legend()

    # Add coastlines and gridlines
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linestyle='--', linewidth=0.5, color='grey')
    #gl.xlabels_top = False
    #gl.ylabels_right = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    
    # Add map features
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAND, edgecolor='black')

    plt.show()



def main():
    pass

if __name__ == '__main__':
    main()