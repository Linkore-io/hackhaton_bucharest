"""python program that opens a series of threads from a list of names and loads a function into each thread"""
import threading
import time
import random

def thread_function(name):
    """thread_function function that prints the name of the thread and sleeps for a random amount of time"""
    print("Thread %s: starting", name)
    time.sleep(random.randint(1, 5))
    print("Thread %s: finishing", name)

if __name__ == "__main__":
    names = ["John", "Eric", "Jessica"]
    threads = list()
    for index in range(3):
        print("Main    : create and start thread %d.", index)
        x = threading.Thread(target=thread_function, args=(names[index],))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        print("Main    : before joining thread %d.", index)
        thread.join()
        print("Main    : thread %d done", index)