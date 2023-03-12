import threading
from abc import abstractmethod
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

    def get_arg_setable(self, name):
        return self.__arg_setables[name]
    
    def notify_arg_set(self, name):
        all_set = True
        for arg_name, arg_setable in self.__arg_setables.items():
            if not arg_setable.is_arg_set():
                all_set = False
                break
        if all_set:
            function_args = {}
            for arg_name, arg_setable in self.__arg_setables.items():
                function_args[arg_name] = arg_setable.consume_arg()
            activatable.activate(function_args, self)
    
    def run(self, **args):
        self.function(**args)

class activatable:
    
    @abstractmethod
    def activate(self, function_args, function):
        pass


class node (activatable):
    def __init__(self, name, functions, ports, activatable):
        self.name = name
        self.functions = functions
        self.ports = ports
        self.activatable = activatable
    
    def activate(self, function_args, function):
        self.activatable.activate(function_args, function)
    
    def add_function(self, name, function):
        self.functions[name] = function
    
    def add_port(self, name, port):
        self.ports[name] = port
    
    def get_port(self, name):
        return self.ports[name]
    
    def add_node_to_function_link(self, node_port_name, function_name, function_port_name):
        node_port = self.get_port(node_port_name)
        function = self.functions[function_name]
        function_port = function.get_arg_setable(function_port_name)
        node_port.add_next_setable(function_port)

    def add_function_to_node_link(self, function_name, function_port_name, node_port_name):
        function = self.functions[function_name]
        function_port = function.get_arg_setable(function_port_name)
        node_port = self.get_port(node_port_name)
        function_port.add_next_setable(node_port)

class thread(activatable):
    def __init__(self, name):
        self.name = name
        self.__nodes = []
        self.__execute_queue = []
        self.thread = threading.Thread(target=self.start)
        self.__lock = threading.Lock()
    
    def add_node(self, node):
        self.__nodes.append(node)

    def get_node(self, name):
        for node in self.__nodes:
            if node.name == name:
                return node
        return None
    
    def run(self):
        self.run_functions()
        self.__lock.acquire()

    def start(self):
        self.thread.start()

    def join(self):
        self.thread.join()

    
    def activate(self, function_args, function):
        self.__execute_queue.append((function, function_args))
        self.__lock.release()

    def consume_function(self):
        return self.__execute_queue.pop(0)
    
    def run_functions(self):
        while self.__execute_queue:
            function, function_args = self.consume_function()
            function.run(**function_args)


def thread_function(name, function, args):
    thread = threading.Thread(target=function, args=args)
    thread.start()
    return thread

def main():
    threads = {}
% for thread in threads.items():
    threads["${thread[0]}"] = thread("${thread[0]}")
    % for node in thread[1]:
    threads["${thread[0]}"].add_node(node("${node}", {}, {}, threads["${thread[0]}"]))
        %for function in nodes[node]["Functions"]:
    threads["${thread[0]}"].get_node("${node}").add_function("${function}", function("${function}", ${function}, threads["ThreadMircea's"].get_node("Node1")))
            % for input in functions[function]["Input"]:
    threads["${thread[0]}"].get_node("${node}").get_function("${function}").add_arg_setable("${input}", function_arg_setable("${input}", threads["${thread[0]}"].get_node("${node}").get_function("${function}")))
            % endfor
        % endfor
    % endfor
% endfor
    return

if __name__ == "__main__":
    main()