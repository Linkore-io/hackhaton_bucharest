import sys
import orjson
import getopt
from mako.template import Template


def help():
    """help function that prints arguments and options"""
    print("Usage: python -m codegen [-h] [-v] [-i] [-o]")
    print("Options and arguments:")
    """example of how to print options and arguments"""
    print("-h, -Prints this help message")
    print("-v, --version -Prints the version of the program")
    print("-i, --input -Input file")
    print("-o, --output -Output file")


def print_version():
    """print_version function that prints the version of the program"""
    print("version")


def main(args=None):
    """main function that parses the command line arguments with getopt and calls the appropriate functions"""
    if args is None:
        args = sys.argv[1:]
    try:
        opts, args = getopt.getopt(args, "hi:o:v", ["help", "version"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            help()
            sys.exit()
        elif o in ("-v", "--version"):
            print_version()
            sys.exit()
        elif o in ("-i", "--input"):
            input = a
        elif o in ("-o", "--output"):
            output = a
        else:
            assert False, "unhandled option"

    codegen = CodeGen(input, output)
    codegen.generate()


"""CodeGen python class that generates the code for the given input file and writes it to the output file"""


class CodeGen:
    def __init__(self, input, output):
        self.input = input
        self.output = output

    def generate(self):
        """generate function that generates the code for the given input file and writes it to the output file"""
        json_dict = self.ingest_json(self.input)
        if not json_dict:
            raise Exception("Error: No JSON dictionary found")

        self.populate_code_sources(json_dict)
        self.populate_functions(json_dict)
        self.populate_nodes(json_dict)
        self.populate_links(json_dict)
        self.populate_threads(json_dict)

        self.construct_source_code(json_dict)

    def populate_code_sources(self, json_dict):
        """populate_code_sources function that populates the private dictionary of code sources"""

        self.__code_sources = self.get_sub_json(json_dict, "Sources")
        if not self.__code_sources:
            raise Exception("Error: No code sources found")

    def populate_functions(self, json_dict):
        """populate_functions function that populates the private dictionary of functions"""
        self.__functions = self.get_sub_json(json_dict, "Functions")
        for function in self.__functions.items():
            self.check_function(function)

    def check_function(self, function):
        """check_function function that checks if the function is valid"""
        if not function[1]["Source"] in self.__code_sources:
            raise Exception("Error: No function source found")

    def populate_nodes(self, json_dict):
        """populate_nodes function that populates the private dictionary of nodes"""
        self.__nodes = self.get_sub_json(json_dict, "Nodes")
        for node in self.__nodes.items():
            self.check_node(node)

    def check_node(self, node):
        """check_node function that checks if the node is valid"""
        for function in node[1]["Functions"]:
            if not function in self.__functions:
                raise Exception("Error: No function found")

        for link in node[1]["Links"]:
            if link["origin"]["type"] == "root":
                if node[0] != link["origin"]["owner"]:
                    raise Exception("Error: Root node does not match")

    def populate_links(self, json_dict):
        """populate_links function that populates the private dictionary of links"""
        self.__links = self.get_sub_json(json_dict, "Links")

    def populate_threads(self, json_dict):
        """populate_threads function that populates the private dictionary of threads"""
        self.__threads = self.get_sub_json(json_dict, "Threads")

    def ingest_json(self, json_file):
        """ingest_json function that takes a json file and returns a dictionary"""
        with open(json_file) as f:
            return orjson.loads(f.read())

    def get_sub_json(self, json_dict, key):
        """get_sub_json function that takes a dictionary and a key and returns the value of the key"""
        return json_dict[key]

    def iterate_json(self, json_dict):
        """iterate_json function that takes a dictionary and iterates over it"""
        for key, value in json_dict.items():
            print(key, value)

    def print_json(self, json_dict):
        """print_json function that takes a dictionary and prints it to the console"""
        print(orjson.dumps(json_dict, option=orjson.OPT_INDENT_2).decode())

    def construct_source_code(self, json_dict):
        """construct_source_code function that takes a source and constructs the source code"""
        template = Template(filename='templates/source.mako')
        output = template.render(sources=self.__code_sources, threads=self.__threads,
              functions=self.__functions, nodes=self.__nodes, links=self.__links)
        """write the output to the output file"""
        with open(self.output, 'w') as f:
            f.write(output)

    """Private dictionary storing nodes and their corresponding functions"""
    __nodes = {}

    """Private dictionary storing functions and their input and output names and types"""
    __functions = {}

    """Private dictionary storing links and their origin and destination"""
    __links = {}

    """Private dictionary storing threads and their nodes"""
    __threads = {}

    """Private dictionary storing code sources and their properties"""
    __code_sources = {}


if __name__ == '__main__':
    main()
