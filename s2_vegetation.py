import input_details
from s2vegetation.download_data import download_data

def main():
    username, password = input_details.username, input_details.password
    latitude, longitude = input_details.latitude, input_details.longitude
    dl_info = download_data(username, password, latitude, longitude)
    print(dl_info)

if __name__ == '__main__':
    main()
