import random
import time
import os
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from IPython.display import clear_output

# this script will download all HTML files containing user anime rating list to a specific folder.
# user id and username was get from scrapping username part before.
# you can configure some stuff on config part below.
# if the script stopped due to error, it will print the last succeed anime ids and you can start again from the last suceed user id by changing the id on the config.

###################
# CONFIG
###################

# output folder
folder = 'data/'
user_path = folder + 'user/'
csv_path = folder + 'result/'

user_link_1 = 'https://myanimelist.net/animelist/'
user_link_2 = '?status=2'

html_file = 'user_'
username_file = 'user.csv'

# setting (user id)
start = 1
end = 20000

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
# GET USERNAME
###################

###################
# SCRAP HTML
###################

def scrap_rating(user_id, username):
    path = f"{user_path}"
    os.makedirs(path, exist_ok=True)
    sleep()
    
    data = requests.get(f"{user_link_1}{username}{user_link_2}")
    data_raw = data.text

    soup = BeautifulSoup(data_raw, "html.parser")
    soup.script.decompose()

    with open(f"{user_path}{html_file}{user_id}.html", "w", encoding="UTF-8") as file:
        file.write(soup.prettify())

def run():
    df = pd.read_csv(f"{csv_path}{username_file}", encoding='utf-8')
    
    for i, row in df.iterrows():
        if(row['user_id'] > end):
            break
        if(row['user_id'] >= start):
            user_id = row['user_id']
            username = row['username']
            try:
                scrap_rating(user_id, username)
                clear_output(wait=True)
                print('success: ', user_id)
            except KeyboardInterrupt:
                break
            except:
                clear_output(wait=True)
                print('error: ', user_id)
                break

    print("done")

run()