import numpy as np
import os, rasterio, time, datetime
from sklearn.externals import joblib

def calculate_indices():
    
    ''' reads the bands and calculates the indices'''
    
    for dirpath, dirnames, files in os.walk(os.path.join('.', 'data')):
        extension = '10m.jp2'
        for name in files:
            if extension and name.lower().endswith(extension):
                if 'b08' in name.lower().split('_'):
                    b8 = os.path.join(dirpath, name)
                elif 'b04' in name.lower().split('_'):
                    b4 = os.path.join(dirpath, name)
                elif 'b03' in name.lower().split('_'):
                    b3 = os.path.join(dirpath, name)
                elif 'b02' in name.lower().split('_'):
                    b2 = os.path.join(dirpath, name)
    
    print('Reading the downloaded bands.')
    with rasterio.open(b2, 'r') as b2_file:
        band_blue = b2_file.read()
    with rasterio.open(b3, 'r') as b3_file:
        band_green = b3_file.read()
    with rasterio.open(b4, 'r') as b4_file:
        band_red = b4_file.read()
    with rasterio.open(b8, 'r') as b8_file:
        band_nir = b8_file.read()
    
    blue = band_blue.astype(float)
    green = band_green.astype(float)
    red = band_red.astype(float)
    nir = band_nir.astype(float)
    
    _,x_res,y_res = blue.shape

    np.seterr(divide='ignore', invalid='ignore')
    
    print('Calculating the indices.')
    tic = time.perf_counter()
    array_stack = np.nan_to_num(np.stack(np.array((((nir - red) / (nir + red)),((green - nir) / (green + nir)),(((2*green)-red-blue)/((2*green)+red+blue)),((nir - red)) / (nir + red + 0.16)))), copy=False, nan=0.)
    toc = time.perf_counter()
    print(f"Finished calculation of indices in {toc - tic:0.4f} seconds")
    
    del blue, green, red, nir
    del band_blue,band_green,band_nir,band_red
    return array_stack, x_res, y_res
    
def classification():
    array_stack, x_res, y_res = calculate_indices()
    joblib_file = os.path.join('.','model',"s2vegetation_model.pkl")
    s2vegetation_model = joblib.load(joblib_file)
    array_stack = np.moveaxis(array_stack, 0, -1)
    array_stack = array_stack.reshape(-1, 4)
    y_pred = s2vegetation_model.predict(array_stack)
    predicted_array = y_pred.reshape(1,x_res,y_res)

    now = datetime.datetime.now()
    date = now.strftime("%Y%m%d")
    number_of_bands, height, width = predicted_array.shape
    profile = {"driver": "JPEG","count": number_of_bands,"height": height,"width": width,"dtype": 'uint8'}
    with rasterio.open(os.path.join('.', 'output', date + '.jpg'), 'w', **profile) as dst:
        dst.write(predicted_array)
    
    del array_stack, y_pred, predicted_array