import schedule
from datetime import datetime
import requests
from bs4 import BeautifulSoup as bs4
import sys
import psycopg2
import concurrent.futures
import json
import time

HOST = "postgres"
DATABASE = "farsroid"
USER = "postgres"
PASSWORD = "pass"

con = psycopg2.connect(host=HOST, database=DATABASE,
                       user=USER, password=PASSWORD)
cur = con.cursor()

UPSERT_QUERY = """INSERT INTO apps(
            fa_name, en_name, last_mod, download_box, googleplay_link, farsroid_link, download_links)
            VALUES(%s, %s, %s, %s, %s, %s, %s) ON CONFLICT(farsroid_link) 
            DO UPDATE SET fa_name=%s, en_name=%s, last_mod=%s, download_box=%s, googleplay_link=%s, farsroid_link=%s, download_links=%s"""

API = "https://www.farsroid.com/api/posts/?ids="


def update_app(app):
    link = app
    try:
        page = requests.get(link)
        soup = bs4(page.content, "html.parser")

        googleplay_link = soup.find("a", class_="shadowed-btn gply-link")
        title = googleplay_link.get("title")
        download_link_app = soup.find_all("a", class_="download-btn")
        downlaod_links = ''
        for i in download_link_app:
            dl = i.get("href")
            storage = i.find("span", class_="txt").text.split(
                " - ")[-1].strip()
            downlaod_links += dl + ' ' + storage + '\n'

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
            else:
                value = value.text

            download_box_info += value.strip() + '\n'

        googleplay_link = googleplay_link.get("data-link").strip()

        en_name = title.split('–')[0].strip()
        fa_name = ''.join(title.split('–')[1:]).strip()

        last_mod = soup.find('ul', class_='post-infs').find_all(
            'li')[1].find('div').find('div').get('data-timestamp')

        cur.execute(UPSERT_QUERY, (fa_name, en_name, last_mod,
                                   json.dumps(download_box_info), googleplay_link, link, json.dumps(
                                       downlaod_links), fa_name, en_name, last_mod,
                                   json.dumps(download_box_info), googleplay_link, link, json.dumps(downlaod_links)))
        con.commit()
    except requests.exceptions.ConnectionError:
        print('can not connect to f{link}', file=sys.stderr)
    except psycopg2.IntegrityError:
        print('integrity error')
    except Exception as e:
        print(e)


def updater():
    updated_apps_url = 'https://www.farsroid.com/today-published-apps/'
    updated_games_url = 'https://www.farsroid.com/today-published-games/'

    updated_apps_link = []
    updated_games_link = []

    r = requests.get(updated_apps_url)
    if r.status_code != 200:
        print('update apps: status code is not 200', file=sys.stderr)
    else:
        soup = bs4(r.content, 'html.parser')
        apps = soup.find(
            'div', class_='post-list-company-grid').find_all('a', class_='abs-fill')
        for app in apps:
            app_link = app.get('href')
            updated_apps_link.append(app_link)
        print(updated_apps_link)
        print(len(updated_apps_link))

    r = requests.get(updated_games_url)
    if r.status_code != 200:
        print('update games: status code is not 200', file=sys.stderr)
    else:
        soup = bs4(r.text, 'html.parser')
        apps = soup.find(
            'div', class_='post-list-company-grid').find_all('a', class_='abs-fill')
        for app in apps:
            game_link = app.get('href')
            updated_games_link.append(game_link)
        print(updated_games_link)
        print(len(updated_games_link))

    max_workers = 20
    with concurrent.futures.ThreadPoolExecutor(max_workers) as thp:
        thp.map(update_app, updated_apps_link)

    with concurrent.futures.ThreadPoolExecutor(max_workers) as thp:
        thp.map(update_app, updated_games_link)


schedule.every().day.at("17:00").do(updater)
print('updater is running')
while True:
    print('updater: time:', datetime.now())
    schedule.run_pending()
    time.sleep(1)
