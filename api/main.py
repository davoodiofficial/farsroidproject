from fastapi import FastAPI
from typing import Union
import psycopg2
import psycopg2.extras

SELECT_QUERY1 = """SELECT * FROM apps WHERE en_name like '%%'||%s||'%%' or fa_name like '%%'||%s||'%%'"""
SELECT_QUERY2 = """SELECT * FROM apps WHERE googleplay_link = %s"""

HOST = "postgres"
DATABASE = "farsroid"
USER = "postgres"
PASSWORD = "pass"

app = FastAPI()


@app.get('/')
def home():
    return {'status': 'fast api is working'}


@app.get('/name/')
def get_app_by_name(fa_name: Union[str, None] = None, en_name: Union[str, None] = None):
    conn = psycopg2.connect(host=HOST, database=DATABASE,
                            user=USER, password=PASSWORD, cursor_factory=psycopg2.extras.RealDictCursor)
    cur = conn.cursor()
    cur.execute(SELECT_QUERY1, (en_name, fa_name))
    app = cur.fetchall()
    conn.close()
    return {'app': app}


@app.get('/url/')
def get_app_by_url(url: Union[str, None] = None):
    conn = psycopg2.connect(host=HOST, database=DATABASE,
                            user=USER, password=PASSWORD, cursor_factory=psycopg2.extras.RealDictCursor)
    cur = conn.cursor()
    cur.execute(SELECT_QUERY2, (url, ))
    app = cur.fetchall()
    conn.close()
    return {'app': app}
