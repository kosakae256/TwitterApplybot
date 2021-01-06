import os
import psycopg2
from psycopg2.extras import DictCursor
from os import environ as env

DATABASE_URL = env["DATABASE_URL"]

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

'''
with conn.cursor(cursor_factory=DictCursor) as cur:
    cur.execute('CREATE TABLE test1db (id serial PRIMARY KEY, name varchar(255),money int);')
conn.commit()
'''

with conn.cursor(cursor_factory=DictCursor) as cur:
    cur.execute("""INSERT INTO test1db (name,money) VALUES('ふぁああああああああああ',233)""")#よくあるやつ
    cur.execute("""INSERT INTO test1db (name,money) VALUES('ふぇええええええええ',1213)""")
conn.commit() #commitしてサーバーを介してようやく反映される
with conn.cursor(cursor_factory=DictCursor) as cur: #cursor_factory=DictCursorこうするとfetchしたときに辞書形式で返してくれて便利
    cur.execute('select * from test1db')
    print(cur.fetchall()) #fetchoneで一個だけ、allでぜんぶどり。多分allだけでいい
