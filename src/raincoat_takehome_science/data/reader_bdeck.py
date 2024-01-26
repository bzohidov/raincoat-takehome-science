#!/usr/bin/env python

import pandas as pd
import os

# from local lib
import src.raincoat_takehome_science.data.convert as convert

COLUMNS = ["BASIN",
                "CY",
                "YYYYMMDDHH",
                "TECHNUM/MIN",
                "TECH",
                "TAU",
                "LATN/S",
                "LONE/W",
                "VMAX",
                "MSLP",
                "TY",
                "RAD",
                "WINDCODE",
                "RAD1",
                "RAD2",
                "RAD3",
                "RAD4",
                "POUTER",
                "ROUTER",
                "RMW",
                "GUSTS",
                "EYE",
                "SUBREGION",
                "MAXSEAS",
                "INITIALS",
                "DIR",
                "SPEED",
                "STORMNAME",
                "DEPTH",
                "SEAS",
                "SEASCODE",
                "SEAS1",
                "SEAS2",
                "SEAS3",
                "SEAS4",
                "USERDEFINED",
                "USERDATA"
                ]


def load_b_deck_file(file_path='data/external/bal152017.dat', skip_rows=2):
    """
    Reads a b-deck file and returns the data as a Pandas DataFrame.

    Parameters:
        - file_path (str): Path to the b-deck file.

        Returns:
        - DataFrame: Read data.
    """
    # read b-deck file
    df = pd.read_csv(file_path,
                        names = COLUMNS,
#                              usecols =
                        index_col = False,
                        header = None,
                        skiprows = skip_rows, # I skipped first two rows just to be consistent with the column numbers because 1st 2 rows do not represent maria hurricane.
                        delimiter = ','
                        )

    return df


def generate_intermediate_data(from_file='data/external/bal152017.dat', to_path='data/interim/'):
    """
    Returns intermediate data.
     This data constitutes the contents of the same data as `external` 
     but has been transformed into the measurement units of SI.
     Note that only the following parameters necessary for further processing are extracted from the file:
     - 

    Parameters:
        - file_path (str): File path representing the original data derived from third party source.
    YYYYMMDDHH, LATN/S, LONE/W, VMAX, RMW, RAD, RAD1, RAD2, RAD3, RAD4

    """
    print('Loading data from {}....'.format(from_file))
    # read bdeck file from file.
    df = load_b_deck_file(from_file)
    
    print('Parameters conversion started ....')
    # Prepare the intermediate data    
    # timestamp in string into datetime
    timestamp = convert.timestamp_str_2_datetime(df['YYYYMMDDHH'])
    
    # lat, long conversion into degree
    latlons = df[['LATN/S', 'LONE/W']].apply(lambda x: convert.convert_latlon_hemi_2_degree(x[0].strip(), 
                                                                                            x[1].strip()),
                                                                                            axis=1,
                                                                                            raw=True)   
    # Vmax, knots -> m/s
    vmax = convert.speed_knots_2_ms(df['VMAX'])
    
    # Rmax, nmi -> meter (radius of maximum wind)
    rmax = convert.nautical_miles_2_meter(df['RMW'])
    
    # radius of specified wind intensity
    rad1234 = convert.speed_knots_2_ms(df[['RAD1', 'RAD2','RAD3','RAD4']])
    
    # RAD, knots -> m/s (RAD - wind intensity for the radii defined in 34, 50, 64 knots)
    rad = convert.speed_knots_2_ms(df['RAD'])

    # Concatenate the converted columns
    newdf = pd.concat((timestamp,latlons, vmax, rmax, rad, rad1234),axis=1)

    # convert (lat, lon) into (x, y)
    xy = latlons.apply(lambda v: convert.latlon_2_xy(v[0], v[1]), axis=1, raw=True)    
    newdf['X'] = xy.iloc[:,0]
    newdf['Y'] = xy.iloc[:,1]

    print('Parameters conversion finished....')

    # Save the processed data set in txt file
    basename = os.path.basename(from_file)
    fullpath = os.path.join(to_path, basename)
    if os.path.exists(fullpath):
        print('File already exists in {}. No need to save!'.format(fullpath))
    else:
        newdf.to_csv(fullpath, index=False)
        print('Intermediate file has been created in `{}`'.format(fullpath))
    
    print('Processed intermediate data has been returned to output....')
    return newdf




# def download_file(url, local_path):
#     """
#     Downloads a file from the given URL and saves it locally.

#     Parameters:
#     - url (str): URL of the file to download.
#     - local_path (str): Local path to save the downloaded file.

#     Returns:
#     - str: Local path to the downloaded file.
#     """

#         # r = requests.get(url, allow_redirects=True,)
#         # r.raise_for_status()  # Raise HTTPError for bad responses
        
#         # to_path = os.path.join(os.getcwd(), local_path)

#         # print('THIS: ', to_path)
#         # with open(to_path, 'wb') as f:
#         #     f.write(r.content)
#         # return to_path
#     try:
#         http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
#         with http.request('GET', url, preload_content=False) as r, open(local_path, 'wb') as out_file:
#             if r.status != 200:
#                 raise Exception(f"Failed to download file, HTTP status code: {r.status}")

#             for data in r.stream():
#                 out_file.write(data)

#         return local_path

#     except Exception as e:
#         raise Exception(f"Error downloading file from {url}: {str(e)}")
