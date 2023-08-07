import random
import time
import os
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from IPython.display import clear_output

# this script will download all HTML files of MAL anime by its id to a specific folder.
# you can configure the anime ids range, html name prefix, output folder on config part below.
# if the script stopped due to error, it will print the last succeed anime ids and you can start again from the last suceed anime id by changing the id on the config.

###################
# CONFIG
###################

# output folder
folder = 'data/'
anime_path = folder + 'anime/'
csv_path = folder + 'result/'

anime_link = 'https://myanimelist.net/anime/'

# html file prefix
html_file = 'anime_'

# setting (anime id)
start = 1
end = 70000

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
# SCRAP HTML
###################

def scrap_anime(anime_id):
    path = f"{anime_path}"
    os.makedirs(path, exist_ok=True)
    sleep()
    
    data = requests.get(f"{anime_link}{anime_id}")
    data_raw = data.text

    soup = BeautifulSoup(data_raw, "html.parser")
    soup.script.decompose()

    with open(f"{anime_path}{html_file}{anime_id}.html", "w", encoding="UTF-8") as file:
        file.write(soup.prettify())

###################
# RUN SCRIPT
###################

def run():
    for i in range(start, (end+1)):
        try:
            scrap_anime(i)
            clear_output(wait=True)
            print('success: ', i)
        except KeyboardInterrupt:
            break
        except:
            clear_output(wait=True)
            print('error: ', i)
            break

    print("done")

run()
