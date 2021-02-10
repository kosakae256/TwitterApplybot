import random
from sendMail import send_mail
import psycopg2
from psycopg2.extras import DictCursor
from os import environ as env
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = env["DATABASE_URL"]
RECEIVE_MAILADRESS = env["RECEIVE_MAILADRESS"]#凍結確認メールの送信先


def rh():
    r = random.randint(0,49)
    """
    word = 'あ い う え お か き く け こ さ し す せ そ た ち つ て と な に ぬ ね の は ひ ふ へ ほ ま み む め も や ゆ よ ら り る れ ろ わ を ん'
    wo = word.split(" ")
    print(wo)
    """
    list = ['あ', 'い', 'う', 'え', 'お', 'か', 'き', 'く', 'け', 'こ', 'さ', 'し', 'す', 'せ', 'そ', 'た', 'ち', 'つ', 'て', 'と', 'な', 'に', 'ぬ', 'ね', 'の', 'は', 'ひ', 'ふ', 'へ', 'ほ', 'ま', 'み', 'む', 'め', 'も', 'や', 'ゆ', 'よ', 'ら', 'り', 'る', 'れ', 'ろ', 'わ', 'を', 'ん']
    r = random.randint(0,45)
    return list[r]


def writefreeze(AIlist,myindex,receive_mailadress):#凍結した旨をAIlistに書き込み(メールも送るよ)
    if AIlist[myindex][6] == True:#AIlistから直接凍結確認、メールの連続送信対策
        print("bot",myindex+1,"は凍結確認メール送信済み")
        return
    AIlist[myindex] = [AIlist[myindex][0],AIlist[myindex][1],AIlist[myindex][2],AIlist[myindex][3],AIlist[myindex][4],AIlist[myindex][5],True]
    print("凍結メール送信")
    #send_mail(receive_mailadress,AIlist[myindex][1] + "は凍結してるかもしれない","件名の通り、ご確認ください。") #送信先、件名、メッセージ うるさいから解除中


def AIlistCreate(database_url):#全てのアカウント情報をdbから引っ張ってくる
    conn = psycopg2.connect(database_url, sslmode='require')#データベース情報とつなぎます
    with conn.cursor(cursor_factory=DictCursor) as cur: #cursor_factory=DictCursorこうするとfetchしたときに辞書形式で返してくれて便利(バグでリスト形式で帰ってくる)
        cur.execute(f'select * from AccountInfo ORDER BY id ASC;')
        AIlist=cur.fetchall()
    return AIlist#懸賞アカウントのOauthなどを全て取ってくる


def WordsCreate(database_url):#全ての検索条件情報をdbから引っ張ってくる
    conn = psycopg2.connect(database_url, sslmode='require')#データベース情報とつなぎます
    with conn.cursor(cursor_factory=DictCursor) as cur: #cursor_factory=DictCursorこうするとfetchしたときに辞書形式で返してくれて便利(バグでリスト形式で帰ってくる)
        cur.execute(f'select * from Words ORDER BY id ASC;')
        Words=cur.fetchall()
    return Words#懸賞アカウントのOauthなどを全て取ってくる


if __name__ == '__main__':
    pass
