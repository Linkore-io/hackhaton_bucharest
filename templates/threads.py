"""python program that opens a series of threads from a list of names and loads a function into each thread"""
import threading
import time
import random

class MyNode:
    def __init__(self, name, function):
        self.name = name
        self.function = function

    def run(self):
        print("Node %s: starting", self.name)
        time.sleep(random.randint(1, 5))
        print("Node %s: finishing", self.name)

class MyThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        print("Thread %s: starting", self.name)
        time.sleep(random.randint(1, 5))
        print("Thread %s: finishing", self.name)

if __name__ == "__main__":
    threads = []
    for i in range(5):
        threads.append(MyThread("Thread-%d" % i))
        threads[-1].start()

    for t in threads:
        t.join()

    print("Main    : All done.")