import threading
import time


def display(name, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print(name, "------", time.time())


class MyThread(threading.Thread):

    def __init__(self, name, delay):
        threading.Thread.__init__(self)
        self.name = name
        self.delay = delay

    def run(self):
        print('start thread')
        display(self.name, self.delay)
        print("end thread")


if __name__ == "__main__":
    t1 = MyThread('Thread1', 1)
    t2 = MyThread('Thread2', 2)

    t1.start()
    t2.start()

    print(t1.getName())
    print(t2.getName())
    print(threading.activeCount())
    print(threading.currentThread())
    print(threading.enumerate())

    t1.join()
    t2.join()


    print("Done")