import threading
import time

total = 4


def create_items_1():
    global total
    for i in range(10):
        time.sleep(2)
        print('creator1 add item')
        total += 1
    print("create_item_1 is done")


def create_items_2():
    global total
    for i in range(7):
        time.sleep(2)
        print('creator2 add item')
        total += 1
    print("create_item_2 is done")


def limit_items():
    global total
    while True:
        if total > 5:
            print('overload')
            total -= 3
            print('subtracted 3')
        else:
            time.sleep(1)
            print('waiting')


creator1 = threading.Thread(target=create_items_1)
creator2 = threading.Thread(target=create_items_2)
limitor = threading.Thread(target=limit_items, daemon=True)

creator1.start()
creator2.start()
limitor.start()

creator1.join()
creator2.join()
