from multiprocessing import Process, Manager
import time

def f(l):
    while True:
        time.sleep(1)
        print(l)

def f3(l):
    while True:
        time.sleep(1)
        print(l[0][0])

def f2(l,i):
    time.sleep(0.1)
    for i in range(0,100):
        l[0][0] = i
        l[0] = [1,2,3]
        print(l)
        time.sleep(1)

if __name__ == '__main__':
    manager = Manager()

    l = manager.list([[1,"おちん",2],[2,"dkfd",2]])
    l2 = manager.list([2,3,2])


    p1 = Process(target=f, args=(l,))
    p1.start()
    p3 = Process(target=f3, args=(l,))
    p3.start()


    while True:
        for i in range(0,100):
            p2 = Process(target=f2, args=(l,i,))
            p2.start()
            p2.join()
