import pandas
import google_image_crawler


DEBUG = False

file_names = ['subscriber_500_upper', 'subscriber_300_upper',
        'subscriber_100_upper', 'subscriber_50_upper', 'subscriber_30_upper', 'subscriber_10_upper']
if DEBUG:
    file_names = ['subscriber_500_upper']
many_csv_data = []
for file_name in file_names:
    csv_data = pandas.read_csv("../data/"+file_name+".csv", header=None)
    if DEBUG:
        print(f"[{file_name}]: {len(csv_data)}")
    for row_idx in range(len(csv_data)):
        channel_name = str(csv_data[1][row_idx])
        google_image_crawler.download_google_staticimages('./chromedriver', f'{channel_name} 유튜브', f'/Volumes/Data/{file_name}/{channel_name}/', 300)
