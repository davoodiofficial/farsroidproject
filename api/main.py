from fastapi import FastAPI
from typing import Union
import sqlite3

SELECT_QUERY = """SELECT * FROM apps WHERE en_name like '%'||?||'%' or fa_name like '%'||?||'%'"""

app = FastAPI()


@app.get('/')
def home():
    return {'status': 'fast api is working'}


@app.get('/name/')
def get_app_by_name(fa_name: Union[str, None] = None, en_name: Union[str, None] = None):
    conn = sqlite3.connect('../crawler/apps.db')
    cur = conn.cursor()
    cur.execute(SELECT_QUERY, (en_name, fa_name))
    app = cur.fetchall()
    cur.execute("select en_name from apps where id = 1")
    print(f"'{cur.fetchall()}'")
    return {'app': app}


@app.get('/url/')
def get_app_by_url(url: Union[str, None] = None):
    return {'app': url}
