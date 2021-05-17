from sentinelsat import SentinelAPI
import zipfile
import os, sys

def check_login(username, password, latitude, longitude):
    
    ''' Checks the login and location details, SentinelAPI queries the Copernicus database '''
    
    if username==None or password==None:
        print('\n Enter Login Details for the Copernicus SciHub\n if not registered, go to:\n https://scihub.copernicus.eu\n')
        username = input('\n Username:  ')
        password = input('\n Password:  ')
        print('\n')
    
    if latitude==None or longitude==None:
        print('Latitude and Longitude in decimal degrees\n')
        try:
            latitude = float(input('\n Latitude:  '))
            longitude = float(input('\n Longitude:  '))
        except:
            print('\n Latitude and Longitude are to be entered in decimal degrees\n Program Terminated\n')
            sys.exit()
        print('\n')
    
    try:
        api = SentinelAPI(username, 
                          password, 'https://scihub.copernicus.eu/dhus')
        footprint = f'POINT ({latitude} {longitude})'
        data_populate = api.query(footprint, date=('NOW-12MONTHS','NOW'), 
                                  order_by='cloudcoverpercentage', 
                                  platformname='Sentinel-2', 
                                  processinglevel='Level-2A', 
                                  cloudcoverpercentage=(0,10))
        data_database = api.to_geodataframe(data_populate)
        return api, data_database
    except:
        print('\n Incorrect Login Details\n Program Terminated')
        sys.exit(1)

def download_data (username, password, latitude, longitude):
    
    ''' download the lowest cloudcoverpercentage tile and extract to data directory'''
    
    api, data_database = check_login(username, password, latitude, longitude)
    data_database_sorted = data_database.sort_values('cloudcoverpercentage', 
                                                 ascending=True).reset_index()
    
    for item in range(len(data_database_sorted)):
        try:
            print("\n Fetching " +data_database_sorted['index'].iloc[item]+ " from SciHub...\n")
            data_download = api.download(data_database_sorted['index'].iloc[item], 
                             directory_path=os.path.join('.', 'data'))
            break
        except:
            continue
    print("\ndownload complete!\n")
    zip = zipfile.ZipFile(os.path.join('.', 'data', 
                                   data_download['title'] + '.zip'))
    zip.extractall(os.path.join('.', 'data'))
    return data_download