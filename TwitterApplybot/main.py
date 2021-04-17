import os
from os import environ as env
import psycopg2
from psycopg2.extras import DictCursor
import time
from multiprocessing import Manager,Value, Process
import tweepy
import datetime
import os.path
from usefullFunctions import rh,writefreeze,AIlistCreate,WordsCreate #自作便利関数ず
from sendMail import send_mail
from TwitterExecute import TwitterExecuteAPI #自作tweepy操作クラス
from dotenv import load_dotenv
load_dotenv()


#並列処理の開始
  #60hunn
  #accountInfoテーブルから全データ取得

DATABASE_URL = env["DATABASE_URL"]
RECEIVE_MAILADRESS = env["RECEIVE_MAILADRESS"]#凍結確認メールの送信先




#アカウントごとの並列処理
#bot
def bot(ID,AIlist,Words):#AIdictにはデータベースを基にしたリストが、idは自分のbot番号(1～x),target_usersは共有リスト、中にフォロー対象者のidを入れる
    myindex = ID-1
    num = 1
    while True:

        try:#謎のエラー対処用
            print(f"RTbot{ID} 実行")



            try:  #アカウントが無かったら先頭から
                AIlist[myindex]
            except IndexError:
                print("アカウントが存在しません")
                time.sleep(30*60)
                continue

            Api = TwitterExecuteAPI(AIlist[myindex],Words) #api操作用,Wordsは検索条件
            if Api.is_freeze() == True:#凍結確認 誤検出対策で凍結してても動作させる
                writefreeze(AIlist,myindex,RECEIVE_MAILADRESS)#AIlist[index][6]にTrueを書き込み、//凍結確認メールを送る
            else: #凍結していなかったら
                AIlist[myindex] = [AIlist[myindex][0],AIlist[myindex][1],AIlist[myindex][2],AIlist[myindex][3],AIlist[myindex][4],AIlist[myindex][5],False]#freezeをfalseに

            follow_count = Api.api.get_user(screen_name=Api.myname).friends_count

            if follow_count == 0:
                time.sleep(30*60)
                print("凍結or制限")
                time.sleep(30*60)
                continue

            if follow_count <= 500:
                print(Api.myname,"follow : (" , follow_count , ")はbot動作条件を満たしていないため、フォローbot化します")
                Api.follow14users()
                time.sleep(60)
                continue

            Api.get_tweets()#懸賞ツイートを取得、情報を格納
            #Api.test()#テストコードの実行
            Api.rt_and_like()#リツイートといいねをするよ

            print(f"RTbot{ID}の処理 {num}回目終了")
            num += 1#起動回数
            Api.targetUsersCreate() #フォローすべき人の最新の28件を作ります

            if num%1 == 0: #1時間に一回フォローをするための処理
                Api.follow() #最新の28人をフォローします
                print(f"Followbot{ID}の処理 {int(num/2)}回目終了")

            if num%4 == 0: #2時間おきに、適当な言葉の羅列をツイートして凍結対策
                Api.api.update_status(rh()+rh()+rh()+rh()+rh()+rh()+rh()+rh()+rh()+rh()+rh()+rh()+rh()+rh()+rh()+rh()+rh()+rh()+rh()+rh()+rh()+rh()+rh()+rh()+rh()+rh()+rh()+rh()+rh()+rh()+rh()+rh()+rh()+rh()+rh()+rh()+rh())
            del Api#メモリ解放
        except:
            print("bot",ID, "原因不明エラー")

        try:
            print(f"RTbot{ID} 待機")
            time.sleep(15*60)#30分待ち、エラーを意図的に起こせばすぐにしたが実行される
        except:
            pass


def updatebot(AIlist,Words):#データベースとメモリを連携させます
    while True:
        try:
            time.sleep(5*60)
                #AIlistの凍結情報をdbに書き込む
            conn = psycopg2.connect(DATABASE_URL, sslmode='require') #データベース情報とつなぎます
            with conn.cursor(cursor_factory=DictCursor) as cur:
                for list in AIlist:
                    cur.execute(f"""UPDATE AccountInfo SET isfreeze = {list[6]} WHERE id={list[0]}""") #書き込むよ
                conn.commit() #しっかりやろう、結果にコミット(これがないせいでバグが発生していた)
            #AIlistのbot情報をデータベースから引っ張ってくる
            AIlistTemp = AIlistCreate(DATABASE_URL) #リスト形式で最新のAIlistを取得
            del AIlist[:]
            del Words[:]
            for list in AIlistTemp:
                    AIlist.append(list)
            #Wordsの中身をdbから更新
            WordsTemp = WordsCreate(DATABASE_URL)#リスト形式で最新のWordsを取得
            for list in WordsTemp:
                    Words.append(list)

            del AIlistTemp
            del WordsTemp
        except:
            print("a")



#最初に実行される。テーブル管理、アカウントごとのRT,Follow並列処理を行う。AIlist,Wordsは共有メモリのリスト
def main():
    manager = Manager()
    AIlist = manager.list(AIlistCreate(DATABASE_URL))#botの情報一式をdbから受け取り、共有メモリに格納
    Words = manager.list(WordsCreate(DATABASE_URL))#検索条件をdbから(上と類似)

    botList=[0 for i in range(0,30)]#botのサブプロセスリスト 今は50個までの制限
    for i in range(0,30):
        time.sleep(10)
        botList[i] = Process(target=bot, args=(i+1,AIlist,Words,))#自分のidと共有メモリのbot情報と共有メモリの検索条件を持つ
        botList[i].start()#RTbot50個を動かす

    updatebotinstance = Process(target=updatebot,args=(AIlist,Words,))#dbと連携して情報をリアルタイムで更新できるようにする(5分ごと)
    updatebotinstance.start()

    #testbotinstance = Process(target=testbot,args=(AIlist,Words,))
    #testbotinstance.start()
    updatebotinstance.join()

def testbot(AIlist,Words):
    while True:
        time.sleep(5)
        print(AIlist,Words)


if '__main__' == __name__:
    main()
