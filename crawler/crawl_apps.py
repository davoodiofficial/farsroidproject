import requests
from bs4 import BeautifulSoup
import sqlite3

DB_NAME = "apps.db"
CREATE_APP_TABLE_QUERY = """CREATE TABLE IF NOT EXISTS apps (
                                    id integer PRIMARY KEY,
                                    fa_name text NOT NULL,
                                    en_name text NOT NULL,
                                    last_mod text NOT NULL,
                                    download_box text NOT NULL,
                                    googleplay_link text NOT NULL UNIQUE,
                                    farsroid_link text NOT NULL UNIQUE
                                );"""
INSERT_APP_QUERY = """INSERT INTO apps(fa_name,en_name,last_mod,download_box,googleplay_link,farsroid_link)
              VALUES(?,?,?,?,?,?)"""

conn = sqlite3.connect(DB_NAME)

cur = conn.cursor()
cur.execute(CREATE_APP_TABLE_QUERY)

URL = "https://www.farsroid.com/chrome-canary-android/"
API = "https://www.farsroid.com/api/posts/?ids="
LAST_MOD = '2023-02-25 16:11'

page = requests.get(URL)
# print(page.status_code)

soup = BeautifulSoup(page.content, "html.parser")
downloadbox = soup.find("table", class_="post-metas-tabeld")
infos = downloadbox.find("tbody")


googleplay_link = soup.find("a", class_="shadowed-btn gply-link")
title = googleplay_link.get("title")

download_box_info = ''

tr = soup.find_all("tr")
for i in tr:  # extract download box info
    key = i.find("th").find_all("span")[1]
    value = i.find("td")
    download_box_info += key.text.strip() + ': '
    if key.text == 'تعداد بازدید':
        value = value.find('span').find('i').get('data-id')
        r = requests.get(API+value)
        value = r.json()['data'][0]['views']
        # print(r.json()['data'][0]['views'])
    else:
        value = value.text

    download_box_info += value.strip() + '\n'
print(download_box_info)

# print(downloadbox.prettify())
googleplay_link = googleplay_link.get("data-link").strip()

en_name_found = True
fa_name_found = False

fa_name = ''
en_name = ''
# Bikes Hill 2.6.0 – بازی مسابقه ای “دوچرخه سواری در تپه ها” اندروید + مود
en_name = title.split('–')[0]
fa_name = ''.join(title.split('–')[1:])

print(fa_name)
cur.execute(INSERT_APP_QUERY, (fa_name, en_name, LAST_MOD,
            download_box_info, googleplay_link, URL))
conn.commit()
conn.close()
