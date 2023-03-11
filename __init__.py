import sys
import mako
import orjson
import getopt


def main(args=None):
    """main function that parses the command line arguments with getopt and calls the appropriate functions"""
    if args is None:
        args = sys.argv[1:]
    try:
        opts, args = getopt.getopt(args, "h", ["help"])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            print("help")
            sys.exit()
        else:
            assert False, "unhandled option"

    print("Hello World")

if __name__ == '__main__':
    main()