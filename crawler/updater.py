import schedule
import sqlite3
from datetime import datetime
import crawl_apps

con = sqlite3.connect("apps.db")
cur = con.cursor()


def updater():
    res = cur.execute("SELECT * FROM apps")
    res = res.fetchall()
    for i in res:
        old_date = datetime.strptime(i[3], '%Y-%m-%d %H:%M:%S')
        if old_date < new_date:
            crawl_apps.crawl_app(i[6], new_date)

updater()