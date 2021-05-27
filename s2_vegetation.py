import input_details
from s2vegetation.download_data import download_data
from s2vegetation.indices import calculate_indices

def main():
    username, password = input_details.username, input_details.password
    latitude, longitude = input_details.latitude, input_details.longitude
    dl_info = download_data(username, password, latitude, longitude)
    #calculate_indices()

if __name__ == '__main__':
    main()
