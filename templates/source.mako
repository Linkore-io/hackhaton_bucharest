import threading
% for source in sources.items():
${source[1]["import"]}
% endfor

class setable:
    @abstractmethod
    def set(self, value):
        pass

class port(setable):
    def __init__(self, name, value=None):
        self.name = name
        self.value = value

    def set(self, value):
        self.value = value
        if self.__next_setables:
            for setable in self.__next_setables:
                setable.set(value)
    
    def add_next_setable(self, setable):
        self.__next_setables.append(setable)
    
    __next_setables = []

class function_arg_setable(setable):
    def __init__(self, name, function):
        self.name = name
        self.function = function
        self.__arg_array = []

    def set(self, value):
        self.__arg_array.append(value)
        function.notify_arg_set(self.name)
    
    def consume_arg(self):
        return self.__arg_array.pop(0)
    
    def get_arg_count(self):
        return len(self.__arg_array)
    
    def is_arg_set(self):
        return self.get_arg_count() > 0

    __arg_array = []


class function:
    def __init__(self, name, function, activatable):
        self.name = name
        self.function = function
        self.__arg_setables = {}
        self.activatable = activatable
    
    def add_arg_setable(self, name, setable):
        self.__arg_setables[name] = setable
    
    def notify_arg_set(self, name):
        all_set = True
        for arg_name, arg_setable in self.__arg_setables.items():
            if not arg_setable.is_arg_set():
                all_set = False
                break
        if all_set:
            for arg_name, arg_setable in self.__arg_setables.items():
                self.function_args[arg_name] = arg_setable.consume_arg()
            activatable.activate(function_args, self)
    
    @abstractmethod
    def run(self, **args):
        self.function(**args)

class activatable:
    
    @abstractmethod
    def activate(self, function_args, function):
        pass



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