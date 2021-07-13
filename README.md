
# Vegetation Regions from Sentinel-2

Extraction of Vegetation regions from Sentinel-2 using Machine Learning, Python.

NCC                        |  SGDClassifier
:-------------------------:|:-------------------------:
![](/screenshots/ncc.jpg)  |  ![](/screenshots/predicted.jpg)


## Installation

Install the following libraries;

sentinelsat, numpy, rasterio, scikit-learn

```bash
  conda install -c conda-forge sentinelsat
  conda install -c anaconda numpy
  conda install -c conda-forge rasterio
  conda install -c anaconda scikit-learn
```

for entire package list refer Requirements.txt

Created and Tested in Anaconda Python 3.8


## Usage
This program uses the copernicus scihub service.

Register at https://scihub.copernicus.eu

The program prompts to input the login details at the time of execution,
but you can feed the details in input_details.py beforehand, by default they will be assigned None.

The required details include:

- username, password for scihub
- latitude, longitude for which S2 tile to grab

```bash
cd S2_Vegetation
python3 s2_vegetation.py
```


## License

[MIT](https://choosealicense.com/licenses/mit/)

  