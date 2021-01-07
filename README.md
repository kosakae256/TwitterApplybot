# TwitterApplybot
twitterで用いる懸賞botを見やすいように作り直しました。初投稿です。


## DATABASE

### ``AccountInfo``

id,user_name,CK_key,CS_key,AT_key,AS_key,isfreeze


### ``RecordDay``

id,money,day


### ``Words``

id,word,isdisc


## main Libs

``tweepy``   v3.9.0   twitterAPI操作

``psycopg2`` v2.8.5   postgresql操作



## easy-explain-of-files
### ``TwitterApplybot / main.py``

自作クラスTwitterExecuteAPIを用いてWordsテーブル上の検索ワードとNGワードを基に懸賞ツイート群の取得。懸賞ツイートを片っ端からリツイート

懸賞ツイートの主をフォロー

アカウントの凍結確認

上記をアカウントごとに並列処理する

データベースと連携、メモリの更新とデータベースの更新を定期的に行う


### ``TwitterApplybot / usefullFunctions.py``

main.pyの補助をする役割


### ``TwitterApplybot / TwitterExecute.py``

twitterAPIを今回の設計向けに改造したクラスが入ったファイル


### ``otherFiles``

デバッグの助けになるかと思って作っただけです

## 補足
### ``Multiprocessingのバグ(?)``

manager.list()を用いたとき

1次のリストであれば想定通りのふるまいをする

2次以上のリスト形式を使うとき、うまく値の更新が行われない


### ``Tweepyについて``

現在更新終了しているためTwitterというライブラリに乗り換えるべき

dmに関連する機能は失われている

