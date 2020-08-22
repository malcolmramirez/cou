import sys

from lang.interpreter import Interpreter


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python3 cou.py [file]")

    else:
        with open(sys.argv[1]) as content:
            intr = Interpreter(content.read())
            intr.interpret()
