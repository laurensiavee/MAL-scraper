import random
import time
import os
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

# this script will download all HTML files of MAL clubs by its id to a specific folder.
# scrap clubs was needed to get MAL user username list.
# you can configure the club ids range, html name prefix, output folder on config part below.
# if the script stopped due to error, it will print the last succeed anime ids and you can start again from the last suceed anime id by changing the id on the config.

###################
# CONFIG
###################

# output folder
folder = 'data/'
club_path = folder + 'club/'
club_list_path = club_path + 'club_list/'
club_members_path = club_path + 'club_members/'
csv_path = folder + 'result/'

club_link_1 = 'https://myanimelist.net/clubs.php?action=view&t=members&id='
club_link_2 = '&show='

club_list_html_file = 'club_'
club_members_html_file = '_page_'

# member count each page
pager = 36

# setting (club id)
start = 1
end = 100

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

def scrap_club(club_id):
    path = f"{club_list_path}"
    os.makedirs(path, exist_ok=True)
    sleep()
    
    data = requests.get(f"{club_link_1}{club_id}")
    data_raw = data.text

    soup = BeautifulSoup(data_raw, "html.parser")
    soup.script.decompose()

    with open(f"{club_list_path}{club_list_html_file}{club_id}.html", "w", encoding="UTF-8") as file:
        file.write(soup.prettify())

###################
# RUN SCRIPT
###################

def run():
    for i in range(start, (end+1)):
        try:
            scrap_club(i)
            print('success: ', i)
        except KeyboardInterrupt:
            break
        except:
            print('error: ', i)
            break 

    print("done")

run()
