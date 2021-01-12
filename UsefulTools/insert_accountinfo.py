#データベースにアカウントのASとか追加しちゃうよ～
#つまり中
import os
import psycopg2
from psycopg2.extras import DictCursor
from os import environ as env
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = env["DATABASE_URL"]

conn = psycopg2.connect(DATABASE_URL, sslmode='require')


with conn.cursor(cursor_factory=DictCursor) as cur:
    cur.execute("""INSERT INTO AccountInfo (user_name,CK_key,CS_key,AT_key,AS_key,isfreeze) VALUES('username','XXXXXXXXXXXXXXXXX','XXXXXXXXXXXXXXX',
'XXXXXXXXXXXXXXXX-XXXXXXXXXXXXXXXXX','XXXXXXXXXXXXXXXXXXXXXXXX',False)""")#よくあるやつ

conn.commit() #commitしてサーバーを介してようやく反映される
