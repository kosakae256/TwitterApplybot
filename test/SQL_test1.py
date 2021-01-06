import os
import psycopg2
from os import environ as env

DATABASE_URL = env["DATABASE_URL"]

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

with get_connection() as conn:
    with conn.cursor() as cur:
        cur.execute('SELECT * FROM users')

        name = "' OR 1=1 --"  # 悪意のあるパラメータ
        cur.execute('SELECT * FROM users WHERE name = %s', (name,))

        print(cur.query)  #=> "SELECT * FROM users WHERE name = ''' OR 1=1 --'"
        #ひとつだけ取得
        cur.execute('SELECT COUNT(1) FROM users')
        (count,) = cur.fetchone()
