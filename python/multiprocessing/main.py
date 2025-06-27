import multiprocessing

import sys
def work(i:int):
    print(i)
    print(__name__)
    print(sys.modules["__main__"].__dict__)
if __name__ == "__main__":
    pool = multiprocessing.Pool(10)
    def func():
        ...
    pool.map(work,range(1,10))
    pool.close()
    print("__MAIN__")
    print(sys.modules["__main__"].__dict__)

    import time
    time.sleep(1)
    print("work finish")