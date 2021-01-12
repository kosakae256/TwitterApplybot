import os
import psycopg2
from psycopg2.extras import DictCursor
from os import environ as env

DATABASE_URL = env["DATABASE_URL"]

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

with conn.cursor(cursor_factory=DictCursor) as cur:
    cur.execute(f"""SELECT * FROM AccountInfo WHERE user_name = 'tinder123'""")
    print(cur.fetchall())
