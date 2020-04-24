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

def download_google_staticimages(driver_path, keyword, dir_path, limit):

    urllib3.disable_warnings(InsecureRequestWarning)

    t0 = time.time()
    wating_time = 0.2
    searchword = keyword
    searchurl = 'https://www.google.com/search?q=' + searchword + '&source=lnms&tbm=isch'
    dirs = dir_path 
    maxcount = limit

    chromedriver = driver_path
    try:
        pathlib.Path(dirs).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Can't access dir_path: {e}")
        sys.exit()

    
    # if not os.path.exists(dirs):
    #     os.mkdir(dirs)

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    # options.add_argument('--headless')

    try:
        browser = webdriver.Chrome(chromedriver, options=options)
    except Exception as e:
        print(f'No found chromedriver in this environment.')
        print(f'Install on your machine. exception: {e}')
        sys.exit()

    browser.set_window_size(1280, 1024)
    try:
        browser.get(searchurl)
        browser.implicitly_wait(10)

        print(f'Getting you a lot of images. This may take a few moments...')

        element = browser.find_element_by_tag_name('body')

        # Scroll down
        #for i in range(30):
        for _ in range(5):
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            browser.implicitly_wait(10)
            # element.send_keys(Keys.PAGE_DOWN)
            time.sleep(wating_time)

        try:
            browser.find_element_by_id('smb').click()
            for _ in range(50):
                browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                browser.implicitly_wait(10)
                # element.send_keys(Keys.PAGE_DOWN)
                time.sleep(wating_time)
        except:
            for _ in range(10):
                # element.send_keys(Keys.PAGE_DOWN)
                browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                browser.implicitly_wait(10)                
                time.sleep(wating_time)

        # Below is in japanese "show more result" sentences. Change this word to your lanaguage if you require.
        browser.find_element_by_xpath('//input[@value="결과 더보기"]').click()
        browser.implicitly_wait(10)
        # Scroll down 2
        for _ in range(5):
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            browser.implicitly_wait(10)
            # element.send_keys(Keys.PAGE_DOWN)
            time.sleep(wating_time)

        try:
            browser.find_element_by_id('smb').click()
            for _ in range(5):
                browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                browser.implicitly_wait(10)
                # element.send_keys(Keys.PAGE_DOWN)
                time.sleep(wating_time)
        except:
            for _ in range(5):
                browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                browser.implicitly_wait(10)
                # element.send_keys(Keys.PAGE_DOWN)
                time.sleep(wating_time)

        print('Page load done...')
        print('Start to download...')

        #elements = browser.find_elements_by_xpath('//div[@id="islrg"]')
        #page_source = elements[0].get_attribute('innerHTML')
        page_source = browser.page_source 

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

        count = 0
        if urls:
            for url in urls:
                if count >= maxcount:
                    break;
                try:
                    res = requests.get(url, verify=False, stream=True)
                    rawdata = res.raw.read()
                    with open(os.path.join(dirs, 'img_' + str(count) + '.jpg'), 'wb') as f:
                        print(f'Downloading ...{keyword} - [{dir_path}/img_{count}]')
                        f.write(rawdata)
                        count += 1
                except Exception as e:
                    print('Failed to write rawdata.')
                    print(e)
    finally:
        browser.quit()

        t1 = time.time()

        total_time = t1 - t0
        print(f'\n')
        print(f'Download completed. [Successful count = {count}].')
        print(f'Total time is {str(total_time)} seconds.')

# Main block
def main(argv):
    
    if argv[1] == "--help":
        print('usage: python3 google_image_crawler [keyword] [dir_path] [limit]')
    download_google_staticimages(argv[1], argv[2], argv[3], argv[4])

if __name__ == '__main__':
    main(sys.argv)
