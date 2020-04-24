from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

import json
import os
import argparse
import sys

import requests
import urllib
import urllib3
from urllib3.exceptions import InsecureRequestWarning
import pathlib
import datetime
import time


class Downloader:
    def __init__(self, driver):
        self.__driver = driver
    
    def download(self, items):

        # https allow
        urllib3.disable_warnings(InsecureRequestWarning)

        # time check start
        start_time = time.time()

        # count download_num
        for item in items:
            count = 0

            # Search Image
            # keywords_in_url = '+'.join(item['keywords'])
            URL = f'https://www.google.com/search?q={item["keyword"]}&source=lnms&tbm=isch'
            PATH = f'{item["download_context"]}/{item["path"]}/{item["keyword"]}'

            # Duplicate check : for continuous download
            if os.path.exists(PATH):
                print(f'Beacuse keyword [{item["keyword"]}] aleardy exist, It was passed')
                continue

            # Load Page
            print(f'Loading Pages. This may take a few moments...')
            self.__driver.get(URL)
            self.__driver.implicitly_wait(10)
            self.__scroll_to_bottom()
            print('Page Scroll done...')
            print('Start to downloading')

            # download path open
            try:
                pathlib.Path(PATH).mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print(f"Can't access dir_path: {e}")
                sys.exit()
                
            # download
            page_source = self.__driver.page_source 

            soup = BeautifulSoup(page_source, 'html.parser')
            images = soup.find_all('img')

            urls = []
            for image in images:
                try:
                    url = image['data-src']
                    if not url.find('https://'):
                        urls.append(url)
                except:
                    try:
                        url = image['src']
                        if not url.find('https://'):
                            urls.append(image['src'])
                    except Exception as e:
                        print(f'No found image sources.')
                        print(e)


            if urls:
                for url in urls:
                    if count >= item['limit']:
                        break;
                    try:
                        res = requests.get(url, verify=False, stream=True)
                        rawdata = res.raw.read()
                        with open(os.path.join(PATH, 'img_' + str(count) + '.jpg'), 'wb') as f:
                            print(f'Downloading ...{item["keyword"]} - [{PATH}/img_{count}]')
                            f.write(rawdata)
                            count += 1
                    except Exception as e:
                        print('Failed to write rawdata.')
                        print(e)
            print(f'Download completed. [Successful count = {count}].')
                        
        # time check end
        end_time = time.time()
        total_time = end_time - start_time
        print(f'Total time is {str(total_time)} seconds.')

    def close(self):
        self.__driver.close()
        self.__driver.quit()
    
    def __scroll_to_bottom(self):
        wating_time = 0.3
        num_of_scroll_down = 8

        for _ in range(num_of_scroll_down):
            self.__driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            self.__driver.implicitly_wait(10)
            time.sleep(wating_time)
        try:
            more_button = self.__driver.find_element_by_xpath('//input[@value="결과 더보기"]')
            more_button.click()
            self.__driver.implicitly_wait(10)
            time.sleep(wating_time)
        except:
            pass

        for _ in range(num_of_scroll_down):
            self.__driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            self.__driver.implicitly_wait(10)
            time.sleep(wating_time)

            
        


def build(config):
    options = webdriver.ChromeOptions()
    if config['headless']:
        options.add_argument('headless')
    if config['disable_gpu']:
        options.add_argument('--disable-gpu')
    options.add_argument(f'window-size={config["window-size"]}')
    options.add_argument('--no-sandbox')
    try:
        driver = webdriver.Chrome(config['driver_path'], options=options)
    except Exception as e:
        print(f'No found chromedriver in this environment.')
        print(f'Install on your machine. exception: {e}')
        sys.exit()

    return Downloader(driver)
    


if __name__ == '__main__':

    config = {
        'driver_path': './chromedriver',
        'headless': True,
        'window-size': '720x480',
        'disable_gpu': True
    }
    items = []
    item = {
        'keyword': '펭수',
        'limit': 20,
        'download_context': "./download",
        'path': "./동물/"
    }
    item_2 ={
        'keyword': '뽀로로',
        'limit': 20,
        'download_context': "./download",
        'path': "./동물/"
    }
    items.append(item)
    downloader = build(config)
    try:
        downloader.download(items)
    finally:
        downloader.close()
        
