import sys

from lang.interpreter import Interpreter


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python3 cou.py [file]")

    else:

        file = sys.argv[1]
        intr = Interpreter()

        with open(file) as content:
            intr.interpret(content.read())
