import random
import time
import os
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

# this script will add user_id to previous csv file containing all username.

###################
# CONFIG
###################

# output folder
folder = 'data/'
club_path = folder + 'club/'
club_list_path = club_path + 'club_list/'
club_members_path = club_path + 'club_members/'
csv_path = folder + 'result/'

club_list_html_file = 'club_'
club_members_html_file = '_page_'
csv_temp_file = 'user_temp.csv'
csv_file = 'user.csv'

###################
# ADD USER ID
###################

def to_csv(row):
    path = f"{csv_path}"
    os.makedirs(path, exist_ok=True)

    f = open(f"{csv_path}{csv_file}", "a", newline='')
    writer = csv.writer(f)
    writer.writerow(row)
    f.close()

def print_user():
    path = f"{csv_path}"
    os.makedirs(path, exist_ok=True)

    f = open(f"{csv_path}{csv_file}", "r", newline='')

    if os.stat(f"{csv_path}{csv_file}").st_size == 0:
        header = ['user_id', 'username']
        to_csv(header)

    df_existing = pd.read_csv(f"{csv_path}{csv_file}", encoding='utf-8')
    return df_existing

def run():
    df_existing = print_user()

    if(df_existing.empty):
        last_user_id = 0
    else:
        last_user_id = len(df_existing)
    last_user_id

    print('done')
    
run()
