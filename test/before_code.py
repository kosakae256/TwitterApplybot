import tweepy
import datetime
import schedule
from time import sleep
import random
import os.path


class Kensyo():
    def __init__(self):
        pass
    def id(self):
        path = os.path.join(os.path.dirname(__file__))
        openfile = open("id_Oauth.txt",'r')
        rawdata = openfile.read()
        openfile.close()
        user_block = rawdata.split('#')
        name_value = {}
        for i in range(0,len(user_block)):
            name = user_block[i].split(':')[0].replace('\n','').replace(' ','')
            CK = user_block[i].split(':')[1].split(',')[0].replace('\n','').replace(' ','')
            CS = user_block[i].split(':')[1].split(',')[1].replace('\n','').replace(' ','')
            AT = user_block[i].split(':')[1].split(',')[2].replace('\n','').replace(' ','')
            AS = user_block[i].split(':')[1].split(',')[3].replace('\n','').replace(' ','')
            NAME = user_block[i].split(':')[0].replace('\n','').replace(' ','')
            name_value[name] = CK,CS,AT,AS,NAME
        return name_value



    def start(self,usd): #初期処理
    #usdで管理
        self.api_tweepy = []#[tweepy.API]
        self.name = []
        for key in usd:
            self.auth = tweepy.OAuthHandler(usd[key][0], usd[key][1])
            self.auth.set_access_token(usd[key][2],usd[key][3])
            self.name.append(usd[key][4])
            #print("d1")
            try:
                self.api_tweepy.append(tweepy.API(self.auth))
            except:
                print("bot break")
#        your_twitter_id = name
#        self.api_tweet = Twitter(auth=OAuth(accessToken, accessSecret, consumerKey, consumerSecret))
#        self.api_tweepy = tweepy.API(self.auth)
        #print(self.api_tweepy)

        def word_data():
            time = datetime.datetime.now()
            today_m = time.month
            today_d = time.day
            path = os.path.join(os.path.dirname(__file__))
            openfile = open("search_word.txt","r",encoding = 'utf-8')
            raw_data = openfile.read()
            openfile.close()
            data = raw_data.split(";")
            word_count = {}
            openfile2 = open("random.txt","r",encoding = "utf-8")
            raw_data2 = openfile2.read()
            openfile2.close()
            random_texts = raw_data2.replace('\n','').split(",")
            #print(random_texts)

            for i in range(0,len(data)):
                text = data[i].split(":")[0].replace('<time>',str(today_m) + '/' + str(today_d)).replace('<random>',str(random_texts[random.randint(0,len(random_texts)-1)])).replace('<random2>',str(random_texts[random.randint(0,len(random_texts)-1)])).replace('\n','')
                count = int(data[i].split(":")[1])
                word_count[text] = count
                #print("検索文字 : " + text)
            return word_count #辞書データだよ
        def search():







            i=1 #アカウントの数のあれ








            word_count = word_data() #調べたい言葉:検索数
            rt_count=0
            follow_count=0
            path = os.path.join(os.path.dirname(__file__))

            open("aaaa.json","w",encoding='utf-8').write(str(self.api_tweepy[i].rate_limit_status()))

            try:
                openfile = open("already_RT_list_" + str(self.name[i]) , "r" , encoding = 'utf-8')
                raw_data = openfile.read()
                openfile.close()
                already_RT_list = raw_data.replace('\n','').replace(" ","").split(",")
            except:
                #print("ファイルエラー")
                already_RT_list=[]
                try:
                    openfile.close()
                except:
                    pass
            openfile = open("already_RT_list_" + str(self.name[i]) , "a" , encoding = 'utf-8')
            already_follow_list = []
            try:
                for friend in tweepy.Cursor(self.api_tweepy[i].friends_ids,str(self.name[i])).items():
                    already_follow_list.append(friend)
            except:
                pass
            print(self.name[i] + "フォロー数 : " + str(len(already_follow_list)))
            try:
                follow_count_ac = 0
                for key in word_count:
                    results = self.api_tweepy[i].search(q=key, locale='ja', count=word_count[key])
                    #print(word_count[key])
                    #print(key)
                    for result in results:
                        try:
                            text = result.text.encode('cp932','ignore').decode('cp932')
                            search_user = text.split(':')[0].split('@')[1]
                        except:
                            search_user = result.user.screen_name
                            #print("special_error : @" + search_user)#search_userを変える
                        try:
                            #print(key)
                            if str(result.id) not in already_RT_list:
                                openfile.write(str(result.id) + ",")
                                #print("rt ???")
                                #print(result.id)
                                already_RT_list.append(str(result.id))
                                self.api_tweepy[i].retweet(result.id)
                                rt_count += 1
                                print(self.name[i] + " → rt_success!!")

                        except:
                            pass
                        try:
                            self.api_tweepy[i].create_favorite(result.id)
                        except:
                            pass
                        try:
                            search_user_name = search_user
                            #
                            search_user = self.api_tweepy[i].get_user(search_user).id
                            #
                            if follow_count_ac <5:
                                if search_user not in already_follow_list:
                                    #print(search_user)
                                    #print("a")
                                    self.api_tweepy[i].create_friendship(search_user) #ここがおかしいみたい
                                    #print("b")
                                    print(str(search_user)  + " / " + search_user_name + '←' + self.name[i] + ' follow')
                                    #print("c")
                                    follow_count+=1
                                    follow_count_ac += 1
                                    already_follow_list.append(search_user)

                        except:
                            pass
                            #print("謎エラー (" + self.name[i] + ") " + search_user_name + "/" + str(search_user))
            except:
                print("起きちゃいけないエラーだよ。認証エラー引っかかってないか確認しよう。→" + self.name[i])
            openfile.close()
            openfile = open("RT_and_Follow.txt","a",encoding='utf-8')
            openfile.write("RT : " + str(rt_count) + '\nFollow : ' + str(follow_count) + "\n")
            print(self.name[i] + " >>> RT : " + str(rt_count) + '\nFollow : ' + str(follow_count))

#ここ実はstart関数の中です
        search()
a = Kensyo()
user_data = a.id()#dict型のname:ck,cs,at,as,Nameを返す
a.start(user_data)
