from sentinelsat import SentinelAPI
import zipfile
import os

def download_data (username, password, latitude, longitude):
    api = SentinelAPI(username, 
                  password, 'https://scihub.copernicus.eu/dhus')
    footprint = f'POINT ({latitude} {longitude})'
    data_populate = api.query(footprint, date=('NOW-12MONTHS','NOW'), 
                          order_by='cloudcoverpercentage', 
                          platformname='Sentinel-2', 
                          processinglevel='Level-2A', 
                          cloudcoverpercentage=(0,10))
    data_database = api.to_geodataframe(data_populate)
    data_database_sorted = data_database.sort_values('cloudcoverpercentage', 
                                                 ascending=True).reset_index()
    print(data_database_sorted['index'].iloc[0])
    print("\ndownloading data... please wait...\n")
    data_download = api.download(data_database_sorted['index'].iloc[0], 
                             directory_path='./data')
    print("\ndownload complete!\n")
    zip = zipfile.ZipFile(os.path.join('.', 'data', 
                                   data_download['title'] + '.zip'))
    zip.extractall('./data')