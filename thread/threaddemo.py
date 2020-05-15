# 一、初识线程
# 二、线程的作用
# 1、节省资源开销
# 2、充分利用CPU资源
# 3、尤其是在GUI中，如果耗时操作不使用线程就会造成程序的阻塞
# 三、后台线程
# 后台线程和前台线程几乎完全相同，只有一处不同，即后台线程不会确保执行环境一直运行。
# 一旦程序中的所有前台线程都停止，系统会停止并关闭所有后台线程。
# 四、自定义线程
#1、继承 Thread类，重写__init__,run方法
#2、启动线程调用start方法
# 五、线程同步与锁
# 多线程对于共享数据需要进行同步处理---通过Lock机制处理
import threading
import time
import sys
import os
tickets = 1000
lock = threading.Lock()


def do_tickets(name):
    global tickets
    with lock:
        while True:
            # lock.acquire()
            if tickets != 0:
                print(name + '卖票')
                tickets -= 1
                print('余票{}张'.format(tickets))
            else:
                print('票已卖完！')
                os._exit(0)
        # lock.release()


def main_task():
    t1 = threading.Thread(target=do_tickets, args=('thread1', ))
    t2 = threading.Thread(target=do_tickets, args=('thread2',))
    t3 = threading.Thread(target=do_tickets, args=('thread3',))
    t1.start()
    t2.start()
    t3.start()


if __name__ == '__main__':
    main_task()