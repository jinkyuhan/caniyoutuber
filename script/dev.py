import os 
import random

PATH = "/Users/jinkyuhan/Developer/caniyoutuber/data/img/subscriber_10_upper/게임/"
dirlist = os.listdir(PATH)

for dir in dirlist:
    dir_name = dir.replace(' ', '\\ ')
    dir_name = PATH + dir_name
    for i in range(10):
        RANDOM = int(random.random() * 1000000)
        source = dir_name + '/' + 'img_' + str(i) + '.jpg'
        target = PATH + str(RANDOM) + '.jpg'
        command = f"mv {source} {target}"
        # print(command)
        os.system(command)
    # for _, _, files in os.walk(dir_name):
    #     for file_name in files:
    #         print(dir_name + '/' + file_name)
    # print(dir_name)
    # for _, _, files in 
    # command = f"cp {PATH}/{dir_name}/* {PATH}/{RANDOM}.jpg"
    # print(command)
    # os.system()