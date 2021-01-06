#とりあえず使ってるテーブルぜんぶ作り直すよ～
import os
import psycopg2
from os import environ as env
from psycopg2.extras import DictCursor

DATABASE_URL = env["DATABASE_URL"]

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

with conn.cursor(cursor_factory=DictCursor) as cur: #cursor_factory=DictCursorこうするとfetchしたときに辞書形式で返してくれて便利
    cur.execute('''DROP TABLE IF EXISTS AccountInfo;''')#テーブルを消して作り直すだけ
    cur.execute('''DROP TABLE IF EXISTS RecordDay;''')
    cur.execute('''DROP TABLE IF EXISTS Words;''')
    cur.execute('''CREATE TABLE AccountInfo (id serial PRIMARY KEY , user_name varchar(32) , CK_key varchar(127) , CS_key varchar(127) , AT_key varchar(127) , AS_key varchar(127) , isfreeze boolean)''')
    cur.execute('''CREATE TABLE RecordDay (id serial PRIMARY KEY , money int ,day date)''')
    cur.execute('''CREATE TABLE Words (id serial PRIMARY KEY , word varchar(127) ,isdisc int)''')#0ならNGワード,1なら検索ワード

conn.commit()#忘れずコミット
