#データベースの中身ぜんぶ見ちゃうよ～
import os
import psycopg2
from psycopg2.extras import DictCursor
from os import environ as env

DATABASE_URL = env["DATABASE_URL"]

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

with conn.cursor(cursor_factory=DictCursor) as cur: #cursor_factory=DictCursorこうするとfetchしたときに辞書形式で返してくれて便利
    cur.execute('select * from AccountInfo;')
    print(cur.fetchall()) #fetchoneで一個だけ、allでぜんぶどり。多分allだけでいい
    cur.execute('select * from RecordDay;')
    print(cur.fetchall())
    cur.execute('select * from Words;')
    print(cur.fetchall())
