import random
import time
import os
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

# this script will download all HTML files of a club member list, based on clubs list scrapped on 3_scrap_club.
# amount of html page can be set on config part below.
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

pager = 36
min_page = 3

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

def get_page_count(club_id):
    with open(f"{club_list_path}{club_list_html_file}{club_id}.html", "r", encoding="UTF-8") as file:
        soup = BeautifulSoup(file, "html.parser")

        sub = soup.find("div", {"id": "content"})
        if sub is None:
            return "Unknown"
        sub2 = soup.find("div", {"class": "borderClass"})
        if sub2 is None:
            return "Unknown"
        sub3 = sub2.text.strip().replace("\n", "").replace("       ", "")

        if '(' not in sub3:
            return "Unknown"
        splitted = sub3.split("(")
        splitted2 = splitted[1].split(")")

        try:
            page = int(splitted2[0])
            return page
        except:
            return 'Unknown'

def scrap_member(club_id, curr_iter):
    curr_page = (curr_iter - 1) * pager 

    path = f"{club_members_path}"
    os.makedirs(path, exist_ok=True)
    sleep()

    data = requests.get(f"{club_link_1}{club_id}{club_link_2}{curr_page}")
    data_raw = data.text

    soup = BeautifulSoup(data_raw, "html.parser")
    soup.script.decompose()

    with open(f"{club_members_path}{club_list_html_file}{club_id}{club_members_html_file}{curr_iter}.html", "w", encoding="UTF-8") as file:
        file.write(soup.prettify())


###################
# RUN SCRIPT
###################

def run():
    for i in range(start, (end+1)):
        if get_page_count(i) != "Unknown":  
            page_count = get_page_count(i)

            start_pg = 1
            end_pg = page_count + 1 

            print('club: ', i, 'page_count = ', page_count)

            if(page_count > min_page):
                for j in range(start_pg, end_pg):
                    try:
                        scrap_member(i, j)
                        print('success: ', i, ',', j)
                    except KeyboardInterrupt:
                        break
                    except:
                        print('error: ', i, ',', j)
                        break

    print("done")

run()
