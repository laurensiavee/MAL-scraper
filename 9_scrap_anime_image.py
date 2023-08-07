import random
import time
import os
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from IPython.display import clear_output
import shutil

# this script download each anime image to a folder
# if the script stopped due to error, it will print the last succeed anime ids and you can start again from the last suceed anime id by changing the id on the config.

###################
# REQUEST TIME
###################

# wait time (to prevent bot behaviour detection)
min = 3 
max = 8

def sleep():
    sleep_time = random.randrange(min, max)
    time.sleep(sleep_time)

###################
# CONFIG
###################

# output folder
folder = 'data/'
anime_img_path = folder + 'anime_img/'
csv_path = folder + 'result/'

csv_file = 'anime.csv'
img_file = 'anime_img_'

# setting (anime id)
start = 1
end = 70000

###################
# SCRAP IMAGE
###################

def scrap_anime_img(anime_id, img_url):
    path = f"{anime_img_path}"
    os.makedirs(path, exist_ok=True)
    sleep()
    
    data = requests.get(f"{img_url}", stream=True)
    data_raw = data.raw

    with open(f"{anime_img_path}{img_file}{anime_id}.jpg", "wb") as file:
        shutil.copyfileobj(data_raw, file)

###################
# RUN SCRIPT
###################

def run():
    df = pd.read_csv(f"{csv_path}{csv_file}", encoding='utf-8')

    for idx, row in df.iterrows():
        curr_anime_id = row['anime_id']
        curr_anime_img_url = row['img']
        if(curr_anime_id >= start and curr_anime_id<= end):
            try:
                scrap_anime_img(curr_anime_id, curr_anime_img_url)
                clear_output(wait=True)
                print('success: ', curr_anime_id)
            except KeyboardInterrupt:
                break
            except:
                clear_output(wait=True)
                print('error: ', curr_anime_id)
                break
        
    print("done")

run()