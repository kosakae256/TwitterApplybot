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

#汚いのはご愛嬌
with conn.cursor(cursor_factory=DictCursor) as cur:#テーブル消してから再追加
    cur.execute("""DROP TABLE IF EXISTS Words;""")
    cur.execute("""CREATE TABLE Words (id serial PRIMARY KEY , word varchar(127) ,isdisc int)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('LINE',0)""")#よくあるやつ 0ならNG,1なら検索
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('Line',0)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('line',0)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('ライン',0)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('裏垢',0)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('ポイント',0)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('女子',0)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('レビュー',0)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('モニター募集',0)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('一次抽選',0)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('簡単',0)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('ありがとう',0)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('交換',0)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('ビジネス',0)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('確率アップ',0)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('メルカリ',0)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('招待',0)""")





    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('google play プレゼント <random> <random2>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('pc プレゼント <time> <random>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('ニンテンド プレゼント <random> <random2>',1)""")

    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('ギフトカード プレゼント <time>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('ギフトカード プレゼント <random>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('ギフトカード プレゼント <random> <random2>',1)""")

    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('iTunes プレゼント <random> <random2>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('iTunes プレゼント <random> <random2>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('iTunes プレゼント <random>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('iTunes プレゼント <random> <random2>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('iTunes プレゼント <random> <random2>',1)""")

    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('Amazonギフト プレゼント <time>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('Amazonギフト プレゼント <time> <random>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('Amazonギフト プレゼント <time> <random> <random2>',1)""")

    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('paypay リツイート <time>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('paypay リツイート <time> <random>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('paypay リツイート <time> <random> <random2>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('paypay フォロー <time>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('paypay フォロー <time> <random>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('paypay フォロー <time> <random> <random2>',1)""")

    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('amazon リツイート <time>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('amazon リツイート <time> <random>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('amazon リツイート <time> <random> <random2>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('amazon フォロー <time>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('amazon フォロー <time> <random>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('amazon フォロー <time> <random> <random2>',1)""")

    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('アマギフ プレゼント <time>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('アマギフ プレゼント <time> <random>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('アマギフ プレゼント <time> <random> <random2>',1)""")

    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('paypay プレゼント <random> <random2>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('paypay プレゼント <random> <random2>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('paypay プレゼント <random> <random2>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('paypay プレゼント <time> <random>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('paypay プレゼント <time> <random> <random2>',1)""")

    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('Amazon プレゼント <random>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('Amazon プレゼント <random>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('Amazon プレゼント <random> <random2>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('Amazon プレゼント <random> <random2>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('Amazon プレゼント <random> <random2>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('Amazon プレゼント <random> <random2>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('Amazon プレゼント <time>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('Amazon プレゼント <time> <random>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('Amazon プレゼント <time> <random>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('Amazon プレゼント <time> <random> <random>',1)""")
    cur.execute("""INSERT INTO Words (word,isdisc) VALUES('Amazon プレゼント <time> <random> <random>',1)""")






conn.commit() #commitしてサーバーを介してようやく反映される
