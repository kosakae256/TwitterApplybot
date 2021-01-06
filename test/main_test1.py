import os
from os import environ as env
import psycopg2
from psycopg2.extras import DictCursor
import time
from multiprocessing import Manager,Value, Process
import tweepy
import datetime
import os.path
from randomhiragana import rh #ランダムにひらがなを返してくれる関数。githubから見てる方、多分これが一番役に立つコードだと思います。
from sendMail import send_mail

#並列処理の開始
  #60hunn
  #accountInfoテーブルから全データ取得

DATABASE_URL = env["DATABASE_URL"]
RECEIVE_MAILADRESS = env["RECEIVE_MAILADRESS"]#凍結確認メールの送信先


class TwitterExecuteAPI():
    def __init__(self,AIlist,words): #TwitterExecuteクラス Falseを返したら凍結してます。api情報を返したら少なくとも凍結はしてないです。
        self.ID = AIlist[0]#db上のid
        self.myname = AIlist[1]#ユーザー名
        CK = AIlist[2]
        CS = AIlist[3]
        AT = AIlist[4]
        AS = AIlist[5]

        auth = tweepy.OAuthHandler(CK, CS)
        auth.set_access_token(AT,AS)
        self.api = tweepy.API(auth)#twitter apiの完成

        self.target_users = [] #フォロー対象者のリスト
        print(self.myname)
        self.words = words


    def rt_and_like(self):#渡されたツイート情報にRTといいねをするよ
        #self.resultsに全部情報が入ってる
        #self.resultsをforで回して、RTといいねをするよ。エラー馬鹿分かりずらいから念のためtryを掛けておく。あとリツイート一回したことあったら処理とばす
        for result in self.results:
            if (result.retweeted == False):#リツイートされていなかったら
                try:
                    self.api.retweet(result.id)
                    #print("リツイートしたよ")
                except:
                    pass

            if (result.favorited == False):#いいねされてなかったら
                try:
                    self.api.create_favorite(result.id)
                except:
                    pass


    def follow28(self):#最新の28人フォローするよ。意地でもフォローするよ。
        print("フォロー対象ユーザー数 : ",len(self.target_users))
        #print(self.target_users)
        if 29 <= len(self.target_users):
            self.target_users = self.target_users[-28:-1]

        for target in self.target_users:
            try:
                self.api.create_friendship(target)
                #print(target)
            except:
                continue
        self.target_users = []


    def get_tweets(self):#いっぱいツイート取ってくるよ(NGワードとかもこの中で処理)
        #NGワードリスト、検索ワードリストはデータベースから情報を取得するよ
        self.discTweet() #self.ngwords,self.searchwordsに情報伝達をする
        #同一ツイートも検知して削除するようにする
        self.resultsCreater()#self.resultsに処理したいツイートを総入れ
        print("ツイート取得数 : ",len(self.results))


    def is_freeze(self):#凍結確認
        #フリーズしてたらTrueをreturnする
        try:
            results = self.api.home_timeline(count=2)
            for result in results:
                self.api.retweet(result.id)
                return False #凍結してない
        except:
            return True #凍結してる


    def test(self):#動いているかてすとするためだけの関数
        print(len(self.results))
        time.sleep(5)
        for result in self.results:
            time.sleep(0.1)
            print(result.text,"\n--------------------------------------------\n")


    def discTweet(self):#searchwordsとngwordsを作ってくれます
        #self.wordsに情報が格納されているのでそれを用いる
        self.ngwords = []
        self.searchwords = []
        for list in self.words:
            if list[2] == 0:#ngワードなら
                self.ngwords.append(list[1])
            elif list[2] == 1:
                time = datetime.datetime.now()
                today_m = time.month
                today_d = time.day
                q = list[1].replace('<time>',str(today_m) + '/' + str(today_d)).replace('<random>',rh()).replace('<random2>',rh()).replace('\n','')
                self.searchwords.append(q)


    def resultsCreater(self):#同一ツイート、NGワードの判定を行って仕分け。のちにself.resultsにして返す
        self.results=[] #取得ツイートの初期化
        self.results_text=[] #同様
        for q in self.searchwords:#検索ワードリストの繰り返し
            try:#謎のエラーが出ることがあるのでこれで対処
                results = self.api.search(q=q,locale='ja', count=100,result_type = "mixed")#検索ワードqを検索
            except:
                print("検索地点でタイムアウトが発生しました")
                continue
            time.sleep(2) #twitter鯖に負荷を掛けないように

            for result in results:
                for ngword in self.ngwords:#ngワードに含まれるか
                    if result.text in ngword:
                        continue

                if (result.text in self.results_text) or (result.is_quote_status == True) or (result.retweeted==True):#今まで見たツイートと同一か、引用ツイートか,自分はこのツイートをすでにRTしているか
                    continue
                self.results_text.append(result.text)
                self.results.append(result)

        results = [] #疑似メモリ解放


    def targetUsersCreate(self): #self.resultsを参考にしてself.target_users(フォロー対象リスト)を生成します
        #self.resultsからフォロー対象者(全員)
        for result in self.results:#RTしたツイートの情報を回します
            try:
                target = result.text.split(':')[0].split('@')[1]#誰がツイートしたのか正確に判別
            except:
                target = result.user.screen_name #target変数にフォロー対象者の名前を格納

            if (result.user.following == False) and (target not in self.target_users) and (target != self.myname): #ユーザーをフォローしていないこと、この処理中に同じ人を指していないか、自分を指していないか
                self.target_users.append(target)
                if self.myname in self.target_users:
                    self.target_users.remove(self.myname) #self.myname(自分)を削除します。これは念のための処置です








def writefreeze(AIlist,myindex):#凍結した旨をAIlistに書き込み(メールも送るよ)
    if AIlist[myindex][6] == True:#AIlistから直接凍結確認、メールの連続送信対策
        return
    AIlist[myindex] = [AIlist[myindex][0],AIlist[myindex][1],AIlist[myindex][2],AIlist[myindex][3],AIlist[myindex][4],AIlist[myindex][5],True]
    print("凍結メール送信")
    send_mail(RECEIVE_MAILADRESS,AIlist[myindex][1] + "は凍結してるかもしれない","件名の通り、ご確認ください。") #送信先、件名、メッセージ


def AIlistCreate():#全てのアカウント情報をdbから引っ張ってくる
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')#データベース情報とつなぎます
    with conn.cursor(cursor_factory=DictCursor) as cur: #cursor_factory=DictCursorこうするとfetchしたときに辞書形式で返してくれて便利(バグでリスト形式で帰ってくる)
        cur.execute(f'select * from AccountInfo;')
        AIlist=cur.fetchall()
    return AIlist#懸賞アカウントのOauthなどを全て取ってくる


def WordsCreate():#全ての検索条件情報をdbから引っ張ってくる
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')#データベース情報とつなぎます
    with conn.cursor(cursor_factory=DictCursor) as cur: #cursor_factory=DictCursorこうするとfetchしたときに辞書形式で返してくれて便利(バグでリスト形式で帰ってくる)
        cur.execute(f'select * from Words;')
        Words=cur.fetchall()
    return Words#懸賞アカウントのOauthなどを全て取ってくる


#アカウントごとの並列処理
#bot
def bot(ID,AIlist,Words):#AIdictにはデータベースを基にしたリストが、idは自分のbot番号(1～x),target_usersは共有リスト、中にフォロー対象者のidを入れる
    myindex = ID-1
    num = 1
    while True:
        try:
            time.sleep(60*30)#30分待ち、エラーを意図的に起こせばすぐにしたが実行される
        except:
            pass

        try:#謎のエラー対処用
            print(f"RTbot{ID} 実行")

            try:  #アカウントが無かったら先頭から
                AIlist[myindex]
            except IndexError:
                print("アカウントが存在しません")
                continue

            Api = TwitterExecuteAPI(AIlist[myindex],Words) #api操作用,Wordsは検索条件
            if Api.is_freeze() == True:#凍結確認 誤検出対策で凍結してても動作させる
                writefreeze(AIlist,myindex)#AIlist[index][6]にTrueを書き込み、凍結確認メールを送る
            else: #凍結していなかったら
                AIlist[myindex] = [AIlist[myindex][0],AIlist[myindex][1],AIlist[myindex][2],AIlist[myindex][3],AIlist[myindex][4],AIlist[myindex][5],False]#freezeをfalseに

            Api.get_tweets()#懸賞ツイートを取得、情報を格納
            #Api.test()#テストコードの実行
            Api.rt_and_like()#リツイートといいねをするよ

            print(f"RTbot{ID}の処理 {num}回目終了")
            num += 1#起動回数
            Api.targetUsersCreate() #フォローすべき人の最新の28件を作ります

            if num%2 == 0: #1時間に一回フォローをするための処理
                Api.follow28() #最新の28人をフォローします
                print(f"Followbot{ID}の処理 {int(num/2)}回目終了")

        except:
            print("bot",ID, "原因不明エラー")


def updatebot(AIlist,Words):#データベースとメモリを連携させます
    while True:
        try:
            time.sleep(60*10)
            #AIlistの凍結情報をdbに書き込む
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')#データベース情報とつなぎます
            with conn.cursor(cursor_factory=DictCursor) as cur:
                for list in AIlist:
                    cur.execute(f"""INSERT INTO AccountInfo(isfreeze) VALUES({list[6]}) WHERE id={list[0]}""") #書き込むよ
            #AIlistのbot情報をデータベースから引っ張ってくる
            AIlist = AIlistCreate()#リスト形式で最新のAIlistを取得
            #Wordsの中身をdbから更新
            Words = WordsCreate()#リスト形式で最新のWordsを取得
        except:
            pass


#最初に実行される。テーブル管理、アカウントごとのRT,Follow並列処理を行う。AIlist,Wordsは共有メモリのリスト
def main():
    manager = Manager()
    AIlist = manager.list(AIlistCreate())#botの情報一式をdbから受け取り、共有メモリに格納
    Words = manager.list(WordsCreate())#検索条件をdbから(上と類似)
    print(AIlist)

    botList=[0 for i in range(0,5)]#botのサブプロセスリスト

    for i in range(0,5):
        time.sleep(5)
        botList[i] = Process(target=bot, args=(i+1,AIlist,Words))#自分のidと共有メモリのbot情報と共有メモリの検索条件を持つ
        botList[i].start()#RTbot50個を動かす

    updatebotinstance = Process(target=updatebot,args=(AIlist,Words,))#dbと連携して情報をリアルタイムで更新できるようにする(10分ごと)
    updatebotinstance.start()
    botList[0].join()




if '__main__' == __name__:
    main()
