from fastapi import FastAPI
from typing import Union
import sqlite3

SELECT_QUERY1 = """SELECT * FROM apps WHERE en_name like '%'||?||'%' or fa_name like '%'||?||'%'"""
SELECT_QUERY2 = """SELECT * FROM apps WHERE googleplay_link = ?"""

app = FastAPI()


@app.get('/')
def home():
    return {'status': 'fast api is working'}


@app.get('/name/')
def get_app_by_name(fa_name: Union[str, None] = None, en_name: Union[str, None] = None):
    conn = sqlite3.connect('../crawler/apps.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(SELECT_QUERY1, (en_name, fa_name))
    app = cur.fetchall()
    conn.close()
    return {'app': app}


@app.get('/url/')
def get_app_by_url(url: Union[str, None] = None):
    conn = sqlite3.connect('../crawler/apps.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(SELECT_QUERY2, (url, ))
    app = cur.fetchall()
    conn.close()
    return {'app': app}
