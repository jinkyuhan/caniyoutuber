import pandas
import gid
import os


config = {
    'driver_path': './chromedriver',
    'headless': False,
    'window-size': '720x480',
    'disable_gpu': False
}

# set up downloader
downloader = gid.build(config)

# open data file
file_names = ['subscriber_500_upper', 'subscriber_300_upper',
        'subscriber_100_upper', 'subscriber_50_upper', 'subscriber_30_upper', 'subscriber_10_upper']
many_csv_data = []
total_data_num = 0
for file_name in file_names:
    csv_data = pandas.read_csv("../data/"+file_name+".csv", header=None)
    channels = []
    for row_idx in range(len(csv_data)):
        channel_name = str(csv_data[1][row_idx])
        category = str(csv_data[2][row_idx])
        channel = {
            'keyword': channel_name + ' 유튜브',
            'limit': 100,
            'download_context': '../data/img',
            'path': f'{file_name}/{category}'
        }
        channels.append(channel)
    # download a file
    downloader.download(channels)


    