import random
import time
import os
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from IPython.display import clear_output

# this script will make a csv files containing user id, anime id, and the rating given by user to the anime
# you will need scraped html of user rating that had been scraped on the step before.
# you can configure some stuff on config part below.

###################
# CONFIG
###################

# output folder
folder = 'data/'
user_path = folder + 'user/'
csv_path = folder + 'result/'

html_file = 'user_'
csv_file = 'rating.csv'

# setting (user id)
start = 1
end = 20000

###################
# TO CSV
###################

def clean(str):
    sp_char = ['\"', '\\']
    for ch in sp_char:
        str = str.replace(ch, "")
    return str

def get_table_data(soup):
    title = soup.find("table", {"class": "list-table"})
    if title is None: 
        return "404"

    raw = title["data-items"]
    soup = BeautifulSoup(raw, "html.parser")
    return soup.text.strip()

def decompose_json(user_id, table_value):
    dict_column = ['tus', 'score', 'is_rewatching', 'num_watched_episodes', 'created_at', 'updated_at', 'anime_title', 'anime_id']

    val = []
    val.append(user_id)

    for col in dict_column:
        splitted_1 = table_value.split(col + "\":")
        splitted_2 = splitted_1[1].split(",")
        clean_str = clean(splitted_2[0])
        if(clean_str == ""):
            clean_str = 'Unknown'
        val.append(clean_str)

    return val

def to_csv(row):
    path = f"{csv_path}"
    os.makedirs(path, exist_ok=True)

    f = open(f"{csv_path}{csv_file}", "a", newline='')
    writer = csv.writer(f)
    writer.writerow(row)
    f.close()

def get_info(user_id):
    with open(f"{user_path}{html_file}{user_id}.html", "r", encoding="UTF-8") as fle:
        soup = BeautifulSoup(fle, "html.parser")

        jsonStr = get_table_data(soup)
        if jsonStr != "404":
            tables = jsonStr.split("{\"sta")
            
            anime_count = len(tables)
            
            for i in range(1, anime_count):
                rating_list = decompose_json(user_id, tables[i])
                if(rating_list!= 'Unknown'):
                    to_csv(rating_list)

            clear_output(wait=True)
            print("success: " + str(user_id))
        else: 
            clear_output(wait=True)
            print("URL not found: " + str(user_id))

def run():
    path = f"{csv_path}"
    os.makedirs(path, exist_ok=True)

    f = open(f"{csv_path}{csv_file}", "w", newline='')

    if os.stat(f"{csv_path}{csv_file}").st_size == 0:
        header = ['user_id', 'score', 'is_rewatching', 'num_watched_episodes', 'created_at', 'updated_at', 'anime_title', 'anime_id']

        to_csv(header)

    for i in range(start, (end + 1)):
        get_info(i)

    print('done')

run()