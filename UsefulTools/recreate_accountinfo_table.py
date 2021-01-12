#データベースのアカウントのASとか全部消しちゃうよ～
import os
import psycopg2
from psycopg2.extras import DictCursor
from os import environ as envfrom dotenv import load_dotenv
load_dotenv()

DATABASE_URL = env["DATABASE_URL"]

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

with conn.cursor(cursor_factory=DictCursor) as cur: #cursor_factory=DictCursorこうするとfetchしたときに辞書形式で返してくれて便利
    cur.execute('''DROP TABLE IF EXISTS AccountInfo;''')#テーブルを消して作り直すだけ
    cur.execute('''CREATE TABLE AccountInfo (id serial PRIMARY KEY , user_name varchar(32) , CK_key varchar(127) , CS_key varchar(127) , AT_key varchar(127) , AS_key varchar(127) , isfreeze boolean)''')
conn.commit()#忘れずコミット
