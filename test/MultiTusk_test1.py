from multiprocessing import Process
import time
# 呼び出したい関数
def f1(name):
    print("Hello", name)
    print("Sleeping... 3s")
    time.sleep(3)
    print("Good morning", name)

if __name__ == "__main__":
    # サブプロセスを作成します
    p = Process(target=f1, args=("Bob",))
    # 開始します
    p.start()
    print("Process started.")
    # サブプロセス終了まで待ちます
    p.join()
    print("Process joined.")
#呼び出す関数の数が膨大で、1つ1つのタスクがライトな場合 -> Processで大量にオブジェクトを生成するのはコストが高いのでPoolを使う。
#呼び出す関数は少ないけど、1つ1つの関数の処理時間が長い場合 -> 単体の生成コストが低いProcessを使う
