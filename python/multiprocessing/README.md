# 基本 API：
```py
from multiprocessing import Process

def f(name):
    print('hello', name)

if __name__ == '__main__':
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()

```
# 启动方法：
https://docs.python.org/3/library/multiprocessing.html#contexts-and-start-methods
- spawn: new interpreter
- fork:
- forkserver

# 进程间信息交换：
pipe,queue
# 进程间 同步，有Lock

 # pool 示例：
 https://docs.python.org/3/library/multiprocessing.html#contexts-and-start-methods  
# 警告：如果不适用with ，那么工作函数放在main外面。pool必须要close()