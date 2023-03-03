import schedule
import sqlite3
from datetime import datetime
import requests
from bs4 import BeautifulSoup as bs4
import sys

con = sqlite3.connect("apps.db")
cur = con.cursor()

API = "https://www.farsroid.com/api/posts/?ids="


def update_app(link, last_mod):
    try:
        page = requests.get(link)
        soup = bs4(page.content, "html.parser")

        googleplay_link = soup.find("a", class_="shadowed-btn gply-link")
        title = googleplay_link.get("title")

        download_links = soup.find_all("a", class_="download-btn")
        for i in download_links:
            dl = i.get("href")
            size = i.find("span", class_="txt").text.split("-")[1].strip()

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

        return f"UPDATE apps SET fa_name = '{fa_name}', en_name = '{en_name}', last_mod = '{last_mod}', download_box = '{download_box_info}', googleplay_link = '{googleplay_link}', farsroid_link = '{link}'"
    except requests.exceptions.ConnectionError:
        print('can not connect to f{link}', file=sys.stderr)
    except sqlite3.IntegrityError:
        pass
    except Exception as e:
        print(e)


def updater():
    updated_apps = str()
    res = cur.execute("SELECT * FROM apps")
    res = res.fetchall()
    for i in res:
        old_date = datetime.strptime(
            i[3], '%Y-%m-%d %H:%M:%S')  # i3 is last mod

        r = requests.get(i[6])  # i6 is farsroid link
        soup = bs4(r.content, 'html.parser')
        data_tiemstamp = soup.find('ul', class_='post-infs').find_all(
            'li')[1].find('div').find('div').get('data-timestamp')
        new_date = datetime.strptime(
            data_tiemstamp, '%Y-%m-%d %H:%M:%S')

        if old_date < new_date:
            update_query = update_app(
                i[6], data_tiemstamp) + f" WHERE id = {i[0]};"
            updated_apps += update_query
            print(update_query)


updater()
