import pandas
import google_image_crawler


DEBUG = True

file_names = ['subscriber_500_upper', 'subscriber_300_upper',
        'subscriber_100_upper', 'subscriber_50_upper', 'subscriber_30_upper', 'subscriber_10_upper']
many_csv_data = []
keywords = ""
for file_name in file_names:
    keywords = []
    csv_data = pandas.read_csv("../data/"+file_name+".csv", header=None)
    if DEBUG == True:
        print(f"[{file_name}]: {len(csv_data)}")
    for row_idx in range(len(csv_data)):
        keywords.append(f', {csv_data[1][row_idx]} 유튜브')
    print(f"[{file_name}] : {keywords}")