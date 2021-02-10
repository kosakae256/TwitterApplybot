import os
import time
import tweepy
import datetime
import os.path
from usefullFunctions import rh

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


    def rt_and_like(self):#渡されたツイート情報にRTといいねをするよ #パッチ1.1.0更新 waitを2.5秒持たせる 連続して処理するとツイッターさんに怒られる
        #self.resultsに全部情報が入ってる
        #self.resultsをforで回して、RTといいねをするよ。エラー馬鹿分かりずらいから念のためtryを掛けておく。あとリツイート一回したことあったら処理とばす
        count=0
        for result in self.results:
            time.sleep(10)
            if (result.retweeted == False):#リツイートされていなかったら
                try:
                    self.api.retweet(result.id)
                    count+=1
                    #print("リツイートしたよ")
                except:
                    pass

            if (result.favorited == False):#いいねされてなかったら
                try:
                    self.api.create_favorite(result.id)
                except:
                    pass
            if count==100:
                break


    def follow(self):#最新の28人フォローするよ。意地でもフォローするよ。 #パッチ1.1.0更新 最大数を28→10に変更 waitを5秒持たせる 安定化とツイート連続取得対策
        print("フォロー対象ユーザー数 : ",len(self.target_users))
        #print(self.target_users)
        if 10 < len(self.target_users):
            self.target_users = self.target_users[-10:-1]

        for target in self.target_users:
            time.sleep(10)
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
            self.api.update_profile(name=self.api.get_user(self.myname).name)
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
            hantei=1
            try:#謎のエラーが出ることがあるのでこれで対処
                time.sleep(5) #twitter鯖に負荷を掛けないように
                results = self.api.search(q=q,locale='ja', count=100,result_type = "mixed")#検索ワードqを検索
            except:
                print("検索地点でタイムアウトが発生しました")
                continue

            for result in results:
                for ngword in self.ngwords:#ngワードに含まれるか
                    if result.text in ngword:
                        hantei=0
                        continue

                if (result.text in self.results_text) or (result.is_quote_status == True) or (result.retweeted==True) or (hantei==0):#今まで見たツイートと同一か、引用ツイートか,自分はこのツイートをすでにRTしているか
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
                    self.target_users.remove(self.myname) #self.myname(自分)をリストから削除します。これは念のための処置です
