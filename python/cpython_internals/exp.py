import threading

a = 0

def func1():
    global a
    for i in range(1000):
        a = a + 1

threadPool = []
for i in range(1000):
    threadPool.append(threading.Thread(target=func1))
for t in threadPool:
    t.start()
for t in threadPool:
    t.join()

print(a)

          
