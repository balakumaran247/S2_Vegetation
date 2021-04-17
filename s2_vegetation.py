from sentinelsat import SentinelAPI
import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiPolygon, Polygon
import numpy as np
import os

import input_details

api = SentinelAPI(input_details.username, input_details.password, 'https://scihub.copernicus.eu/dhus')

footprint = f'POINT ({input_details.latitude} {input_details.longitude})'
print(footprint)

data_populate = api.query(footprint, date=('NOW-12MONTHS','NOW'), order_by='cloudcoverpercentage', platformname='Sentinel-2', processinglevel='Level-2A', cloudcoverpercentage=(0,10))
print(len(data_populate))

data_database = api.to_geodataframe(data_populate)
print(data_database)