import input_details
from s2vegetation.download_data import download_data

def main():
    username, password = input_details.username, input_details.password
    latitude, longitude = input_details.latitude, input_details.longitude
    download_data(username, password, latitude, longitude)

if __name__ == '__main__':
    main()
