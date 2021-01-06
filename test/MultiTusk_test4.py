from multiprocessing import Process, Manager

def f(d):
    d[1] += '1'
    d['2'] += 2

if __name__ == '__main__':
    manager = Manager()

    d = manager.dict()
    d[1] = '1'
    d['2'] = 2

    p1 = Process(target=f, args=(d,))
    p2 = Process(target=f, args=(d,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    print d
 #{1: '111', '2': 6}
# di = manager.dict({0: 1, 1: [1], 2: [1], 3: manager.list([1])})
