from google_images_download import google_images_download   #importing the library
import pandas


DEBUG = True


file_names = ['subscriber_500_upper', 'subscriber_300_upper',
        'subscriber_100_upper', 'subscriber_50_upper', 'subscriber_30_upper', 'subscriber_10_upper']
many_csv_data = []
keywords = ""
for file_name in file_names:
    keywords = ""
    csv_data = pandas.read_csv("../data/"+file_name+".csv", header=None)
    if DEBUG == True:
        print(f"[{file_name}]: {len(csv_data)}")
    for row_idx in range(len(csv_data)):
        keywords += f", {csv_data[1][row_idx]} 유튜브"
    print(f"[{file_name}] : {keywords}")
    
    
    


# google image search and download
response = google_images_download.googleimagesdownload()   #class instantiation

arguments = {"keywords": "워너원 강다니엘","limit":20,"print_urls":True, "format":"jpg"}   #creating list of arguments

paths = response.download(arguments)   #passing the arguments to the function
print(paths)   #printing absolute paths of the downloaded images