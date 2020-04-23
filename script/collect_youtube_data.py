from bs4 import BeautifulSoup
import requests as req
import json
import csv
import re

DEBUG = False

# file open
if DEBUG == False:
    file_names = ['subscriber_500_upper', 'subscriber_300_upper',
        'subscriber_100_upper', 'subscriber_50_upper', 'subscriber_30_upper', 'subscriber_10_upper']
    files = []
    csv_writers = {}
    for file_name in file_names:
        temp = open('../data/' + file_name + '.csv', 'w', encoding='utf-8')
        files.append(temp)
        csv_writers[file_name] = csv.writer(temp)

subjects = ["게임", "BJ%2F인물%2F연예인", "음악%2F댄스%2F가수", "TV%2F방송", "음식%2F요리%2F레시피", "패션%2F미용",
              "뉴스%2F정치%2F사회", "취미%2F라이프", "IT%2F기술%2F컴퓨터", "교육%2F강의", "영화%2F만화%2F애니", "키즈%2F어린이", "애완%2F반려동물", "스포츠%2F운동", "국내%2F해외%2F여행","자동차","주식%2F경제%2F부동산",]
korean = re.compile('[\u3131-\u3163\uac00-\ud7a3]+')
for subject in subjects:
    is_last = False
    for page_num in range(1, 10):
        # Send http request to target URL
        URL = "https://youtube-rank.com/board/bbs/board.php?bo_table=youtube&sca="+subject+"&page=" + \
            str(page_num)
        res = req.get(URL)

        # step2: Parse and process data with BeautifulSoup
        soup = BeautifulSoup(res.text, "html.parser")

        
        youtubers = soup.select(
            "#list-skin > form:nth-child(4) > table > tbody > tr")
        for i in range(len(youtubers)):
            channel_name = youtubers[i].select('.subject > h1 > a')[
                                            0].get_text().strip()
            category = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '',
                            youtubers[i].select('.subject > h1 > .category > a')[0].get_text().strip())
            subscriber = int(re.sub(korean,'',youtubers[i].select('.subscriber_cnt')[0].get_text().strip()))
            if DEBUG == True:
                print('['+subject+']'+channel_name, category, subscriber)
            else:
                if subscriber >= 500:
                    csv_writers['subscriber_500_upper'].writerow([i, channel_name, category, subscriber])
                elif subscriber >= 300:
                    csv_writers['subscriber_300_upper'].writerow([i, channel_name, category, subscriber])
                elif subscriber >= 100:
                    csv_writers['subscriber_100_upper'].writerow([i, channel_name, category, subscriber])
                elif subscriber >= 50:
                    csv_writers['subscriber_50_upper'].writerow([i, channel_name, category, subscriber])
                elif subscriber >= 30:
                    csv_writers['subscriber_30_upper'].writerow([i, channel_name, category, subscriber])
                elif subscriber >= 10:
                    csv_writers['subscriber_10_upper'].writerow([i, channel_name, category, subscriber])
                else:
                    is_last = True
                    break;
        if is_last:
            print(subject, "done")
            break;
    # for file in files:
    #     file.close()

        
