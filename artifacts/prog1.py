import threading
import sys
import time

class function:
    def __init__(self, name, function, args):
        self.name = name
        self.function = function
        self.args = args

    def run(self):
        self.function(*self.args)

class thread:
    def __init__(self, name, function, args):
        self.name = name
        self.function = function
        self.args = args
        self.thread = threading.Thread(target=self.run)

    def run(self):
        self.function(*self.args)

    def start(self):
        self.thread.start()

    def join(self):
        self.thread.join()
    
    __nodes = []

def thread_function(name, function, args):
    thread = threading.Thread(target=function, args=args)
    thread.start()
    return thread

def main():
    return

if __name__ == "__main__":
    main()