import random
import time
import os
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from IPython.display import clear_output

# this script will list all username from scarped html club members.
# the result will be a csv files contained all username.

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

min_page = 1

# setting (club id)
start = 51
end = 60
        
###################
# TO CSV (NO USER ID)
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
        
def to_csv_temp(row):
    path = f"{csv_path}"
    os.makedirs(path, exist_ok=True)

    f = open(f"{csv_path}{csv_temp_file}", "w", newline='')
    writer = csv.writer(f)
    writer.writerow(row)
    f.close()

def get_member_list(soup):
    users = []

    for user in soup.find_all("div", {"style": "margin-bottom: 7px;"}):
        users.append(user.find("a").text.strip())

    return users

def get_info(club_id):
    if get_page_count(club_id) != "Unknown":  
        page_count = get_page_count(club_id)
        
        if(page_count > min_page):
            start_pg = 1
            end_pg = page_count

            for i in range (start_pg, end_pg + 1):
                with open(f"{club_members_path}{club_list_html_file}{club_id}{club_members_html_file}{i}.html", "r", encoding="UTF-8") as file:
                    soup = BeautifulSoup(file, "html.parser")
                    member_list = get_member_list(soup)

                    for member in member_list:
                        to_csv_temp([member])
                
                print("success: " + str(club_id) + ', ' + str(i))
            
            clear_output(wait=True)
            print("success: " + str(club_id))
            

###################
# RUN
###################

def print_all_username():
    path = f"{csv_path}"
    os.makedirs(path, exist_ok=True)

    f = open(f"{csv_path}{csv_file}", "w", newline='')

    if os.stat(f"{csv_path}{csv_file}").st_size == 0:  
        header_temp = ['username']
        to_csv_temp(header_temp)

    for i in range(start, (end + 1)):
        get_info(i)

    print('done print')

def drop_duplicate_username():
    df = pd.read_csv(f"{csv_path}{csv_temp_file}", encoding='utf-8')
    df = df.drop_duplicates()

def run():
    print_all_username()
    drop_duplicate_username()
    print('done')

run()