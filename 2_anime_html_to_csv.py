import random
import time
import os
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from IPython.display import clear_output

# this script will convert all downloaded HTML files to csv.
# you can configure html file location on config.
# you can configure anime ids.

###################
# CONFIG
###################

# input & output folder
folder = 'data/'
anime_path = folder + 'anime/'
csv_path = folder + 'result/'

html_file = 'anime_'
csv_file = 'anime.csv'

# setting (anime id)
start = 1
end = 70000

# variable used on method to contain all special char
sp_char = ['\u2606', '\u2665', 'ヒカリ・新たなる旅立ち', 'ニビジム・史上最大の危機', 'リルル', '카프 박사', 
'\u266a', '\u2605', '\u2060', '\u2661', '\u014d', 'ウル祭', '\u2162', '\u016b', '朗読少年', '朗読兄弟', 'もう一つのエンディング~囚われの安藤なつ',
'\uff0d', '\u03bc', 'アニメ', 'コミック レンタマン', '\u30fb', '\u200b', '坂本渉太', '[謎の老婆]', '[名奉行文さん]', '[女警部神宮寺葉子]',
'[鈴森なんでも相談所]', '(', ')', '[', ']', '少女病', '照英', '鎮座', 'チャンプ&アップル', 'ワンルーム叙事詩', '飯野真澄', '今井弓子',
'\u2192', '永倉新八最強伝説', '夏のわずらい', '\u03a8', 'ラマーズP', 'バカじゃ勝てないのよ', '小沢昭巳', 'キルミーベイベースーパー',
'男宣言', '\u221e', '潔純真夜', '\u2423', '\u300c', '\u300d', '\u014c', '\u2190', '…', '―', '\u25ce', '\u03b8', 'マドンナ 気持ちいい事して下さい。', '姉＆妹 気持ちいい事して下さい。',
',', '\u221a', '\u0394', 'ハーバーテイル', '猪子育代', '赤猫', '水猫', 'カルマ', '鈴木伸一', 'しおこんぶ', '青春ミッドナイトランナーズ', '潮騒',
'\uff0a', 'キドアイ', 'ぶんけかな', '真依子', '\u03b3', '\u03b1', '手塚治虫世紀末へのメッセージ', '\u266d', '\u308b', 'のりのりのりスタ', '◯',
'青青草原', '\u0101', '白雪とゼン、はじめての城下町デート', 'ラジ王子幼少のみぎり', '始まりのゼン＆ミツヒデ＆木々', '\u2103', '\u30fc', '古事記ガル 日向路を旅す',
'愛里寿ウォ', '秋山優花里の戦車講座', '\uff01', 'メグとパトロン', '\u0103', 'サカモト教授', '大月壮', '\u0113', '上野武夫', '鳥羽和一',
'\u0144', '\u011f', '\u2642', '\u25b3', '\uffe5', '\uff1d', '\u03c7', 'ドラマ ~ もぐりこんだら ハム太郎:', 'ハムちゃんずコナ ~ つぼの中のビスケット:',
'ドラマ ~ 大好き、なつみちゃん:', 'ハムちゃんずコナ ~ 黄色いしあわせ:', '\u2191', '\u25cb', 'めろぉ', '\u2934', '八王子P', '\uff0c',
'\u2260', '三叉路', 'おとぎ話', '楠トシエ', '川橋啓史', '大塚佳子', '未来の人へ', '＿', '\u03cc', '我喜屋位瑳務', 'マイスロ', '"はじまり"',
'猪猪侠', 'グ～ン', '\u2159', 'きんだてれび', '\uff08', '\uff09', '\u25c6', '\u222c', '\u2500', '\ufb01', '\ufb00', '天工', '\uff5e',
'\u013b', '\uff0b', '\u0179', '\u03b5', '\u03a6', '\u03a9', 'ズルッグとミミッキュ', 'ユメノツボミ', 'まっててねコイキング', 'ぽかぽかマグマッグハウス',
'ふぶきのなつやすみ', 'プリンのうた', 'ヒロになりたいヤンチャム', 'ゲンガになっちゃった？', '\uff06', '\uff1a', '\u012b', '\u2640', '魔法',
'- シオン', '\uff62', '\uff63', '\u042f', '\u043e', '\ufe0f', '\u25bd', '\u2032', '\u207f', '\u200e', '\u2028', '潟ちゅぶ',
'"สิ่งที่ตี๋ไม่มีวันลืม"', '🌊', '\u0142', '\u041e']

###################
# STRIPPING DATA
###################
def get_title(soup):
    title = soup.find("h1", {"class": "title-name h1_bold_none"})
    if title is None:
        return "404"
    return title.text.strip()

def get_rating(soup):
    rating = soup.find("span", {"itemprop": "ratingValue"})
    if rating is None:
        return "Unknown"
    return rating.text.strip()

def get_rating_count(soup):
    rating_count = soup.find("span", {"itemprop": "ratingCount"})
    if rating_count is None:
        return "Unknown"
    return rating_count.text.strip()

def get_ranked(soup):
    sub = soup.find("span", {"class": "numbers ranked"})
    if sub is None:
        return "Unknown"
    ranked = sub.find("strong")
    if ranked is None:
        return "Unknown"
    return ranked.text.strip().replace("#", "")

def get_popularity(soup):
    sub = soup.find("span", {"class": "numbers popularity"})
    if sub is None:
        return "Unknown"
    popularity = sub.find("strong")
    if popularity is None:
        return "Unknown"
    return popularity.text.strip().replace("#", "")

def get_members(soup):
    sub = soup.find("span", {"class": "numbers members"})
    if sub is None:
        return "Unknown"
    members = sub.find("strong")
    if members is None:
        return "Unknown"
    return members.text.strip().replace(",", "")

def get_season_aired(soup):
    sub = soup.find("span", {"class": "information members"})
    if sub is None:
        return "Unknown"
    season = sub.find("a")
    if season is None:
        return "Unknown"
    return season.text.strip()

def get_type(soup):
    sub = soup.find("span", {"class": "information type"})
    if sub is None:
        return "Unknown"
    type = sub.find("a")
    if type is None:
        return "Unknown"
    return type.text.strip()

def get_studio(soup):
    sub = soup.find("span", {"class": "information studio author"})
    if sub is None:
        return "Unknown"
    type = sub.find("a")
    if type is None:
        return "Unknown"
    return type.text.strip()

def get_synopsis(soup):
    synopsis = soup.find("p", {"itemprop": "description"})
    if synopsis is None:
        return "Unknown"
    syn = synopsis.text.strip().replace("\n", "").replace("<br/", "").replace("[Written by MAL Rewrite]", "").replace("                            ", "")
    if "(Source:" in syn:
        splitted = syn.split("(Source:")
        syn = splitted[0]
    return syn

def get_eps(soup):
    eps = soup.find("span", {"id": "curEps"})
    if eps is None:
        return "Unknown"
    return eps.text.strip()

def get_genre(soup):
    genres = []

    for genre in soup.find_all("span", {"itemprop": "genre"}):
        genres.append(genre.text.strip())

    if len(genres) == 0:
        return "Unknown"
    return genres

def get_url(soup):
    url = soup.find("meta", {"property": "og:url"})
    return url["content"]

def get_img(soup):
    url = soup.find("meta", {"property": "og:image"})
    return url["content"]

###################
# CONVERT TO CSV
###################

def clean(str):
    for ch in sp_char:
        str = str.replace(ch, "")
    return str

def to_csv(row):
    path = f"{csv_path}"
    os.makedirs(path, exist_ok=True)

    f = open(f"{csv_path}{csv_file}", "a", newline='')
    writer = csv.writer(f)
    writer.writerow(row)
    f.close()

def create_header():
    path = f"{csv_path}"
    os.makedirs(path, exist_ok=True)

    f = open(f"{csv_path}{csv_file}", "w", newline='')

    if os.stat(f"{csv_path}{csv_file}").st_size == 0:
        header = ['anime_id', 'title', 'anime_rating', 'rating_count', 'ranked', 'popularity', 'members', 'season_aired', 'type', 'studio', 'synopsis', 'episode_count', 'genre', 'url', 'img']
        to_csv(header)

def get_info(anime_id):
    with open(f"{anime_path}{html_file}{anime_id}.html", "r", encoding="UTF-8") as file:
        soup = BeautifulSoup(file, "html.parser")

        title = get_title(soup)
        if(title != "404"):
            row = []

            row.append(anime_id)
            row.append(clean(get_title(soup)))
            row.append(clean(get_rating(soup)))
            row.append(clean(get_rating_count(soup)))
            row.append(clean(get_ranked(soup)))
            row.append(clean(get_popularity(soup)))
            row.append(clean(get_members(soup)))
            row.append(clean(get_season_aired(soup)))
            row.append(clean(get_type(soup)))
            row.append(clean(get_studio(soup)))
            row.append(clean(get_synopsis(soup)))
            row.append(clean(get_eps(soup)))
            row.append(get_genre(soup))
            row.append(clean(get_url(soup)))
            row.append(clean(get_img(soup)))

            to_csv(row)

            clear_output(wait=True)
            print("success: " + str(anime_id))

        else:
            clear_output(wait=True)
            print("URL not found: " + str(anime_id))

###################
# RUN SCRIPT
###################

def run():
    create_header()

    for i in range(start, (end + 1)):
        get_info(i)

    print('done')    

    # check csv:
    # df = pd.read_csv(f"{csv_path}{csv_file}", encoding='utf-8')
    # df.head()
    
    # df = df.drop_duplicates(subset='anime_id')
    # df.count()

run()