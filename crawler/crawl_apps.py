import requests
from bs4 import BeautifulSoup
import psycopg2
import sys

HOST = "localhost"
DATABASE = "farsroid"
USER = "postgres"
PASSWORD = "pass"
API = "https://www.farsroid.com/api/posts/?ids="
CREATE_APP_TABLE_QUERY = """CREATE TABLE IF NOT EXISTS apps (
                                    id integer PRIMARY KEY,
                                    fa_name text NOT NULL,
                                    en_name text NOT NULL,
                                    last_mod text NOT NULL,
                                    download_box text NOT NULL,
                                    googleplay_link text NOT NULL UNIQUE,
                                    farsroid_link text NOT NULL UNIQUE,
                                    download_links text NOT NULL
                                );"""
INSERT_APP_QUERY = """INSERT INTO apps(
	fa_name, en_name, last_mod, download_box, googleplay_link, farsroid_link, download_links)
	VALUES (%s, %s, %s, %s, %s, %s, %s);"""


def crawl_app(link, last_mod):
    global cur
    global conn

    try:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, "html.parser")

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

        # Bikes Hill 2.6.0 – بازی مسابقه ای “دوچرخه سواری در تپه ها” اندروید + مود
        en_name = title.split('–')[0].strip()
        fa_name = ''.join(title.split('–')[1:]).strip()

        cur.execute(INSERT_APP_QUERY, (fa_name, en_name, last_mod,
                                       download_box_info, googleplay_link, link, downlaod_links))
        conn.commit()
    except requests.exceptions.ConnectionError:
        print('can not connect to f{link}', file=sys.stderr)
    except psycopg2.IntegrityError:
        pass
    except Exception as e:
        print(e)
        conn.rollback()
    else:
        print('inserted:', link, flush=True)


if __name__ == "__main__":
    conn = psycopg2.connect(host=HOST, database=DATABASE,
                            user=USER, password=PASSWORD)
    cur = conn.cursor()
    print("PostgreSQL server information")
    print(conn.get_dsn_parameters(), "\n")
    with open('links.txt', 'r') as file:
        for app in file.readlines():
            app = app.strip().split(' ')  # app link, date, time seprated by space
            link = app[0]
            last_mod = app[1] + ' ' + app[2]
            crawl_app(link, last_mod)
    conn.close()
    exit(0)
