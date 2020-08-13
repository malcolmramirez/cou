import tokens as tkns

from collections import defaultdict
from math import floor

from lexer import Token, Lexer
from parser import AST, Parser

# Interpreter

class Visitor(object):
    """
    Superclass that calls methods used to visit certain nodes on the AST.
    Subclasses will implement these methods in order to traverse the tree
    properly
    """

    def visit(self, node: AST) -> AST:
        """
        Calls appropriate visit method for a node type
        """

        return getattr(self, node.name(), self.error)(node)


    def error(self, node: AST):
        """
        Raises error if no visit method for a node type
        """

        raise ValueError("No visit method for node type: {}", node.name())


class Interpreter(Visitor):
    """
    Evaluates expressions from the parser
    """

    def __init__(self, text: str):
        """
        Initializes interpreter with a parser, used to eval. expressions
        """

        self.parser = Parser(Lexer(text))
        self.sym_tab = defaultdict()


    def syntax_error(self, syntax: object):
        """
        Raises syntax error
        """

        raise TypeError("Invalid syntax \"" + str(syntax) + "\"")


    def number(self, node: AST) -> int:
        """
        Visits a number node (just needs to return the value)
        """

        return node.value()


    def unary_operator(self, node: AST) -> int:
        """
        Visits a unary operator (can only be +/-)
        """

        type = node.type()

        if type == tkns.ADD:
            return self.visit(node.child)

        if type == tkns.SUB:
            return -self.visit(node.child)

        if type == tkns.FLOOR:
            return floor(self.visit(node.child))

        self.syntax_error(type)


    def binary_operator(self, node: AST) -> int:
        """
        Visits a binary operator node on the AST (will recur until a number is
        retrieved)
        """

        type = node.type()

        if type == tkns.ADD:
            return self.visit(node.left) + self.visit(node.right)

        if type == tkns.SUB:
            return self.visit(node.left) - self.visit(node.right)

        if type == tkns.MUL:
            return self.visit(node.left) * self.visit(node.right)

        if type == tkns.DIV:
            return self.visit(node.left) / self.visit(node.right)

        if type == tkns.I_DIV:
            return self.visit(node.left) // self.visit(node.right)

        self.syntax_error(type)


    def variable(self, node: AST) -> AST:
        """
        Interprets a variable
        """

        sym = node.sym()

        if sym not in self.sym_tab:
            raise NameError("Variable \"" + sym + "\" referenced before assignment")

        return self.sym_tab[sym]


    def assignment_statement(self, node: AST) -> None:
        """
        Interprets an assignment statement
        """

        var = node.left.sym()
        self.sym_tab[var] = self.visit(node.right)


    def compound_statement(self, node: AST) -> None:
        """
        Interprets an assignment statement
        """

        for child in node.children:
            self.visit(child)


    def empty(self, node: AST) -> None:
        return


    def interpret(self) -> str:
        """
        Interprets an expression.
        """

        self.visit(self.parser.program())

        return str(self.sym_tab)


def main():

    while True:

        try:
            file_name = input("> ")
            text = ''

            with open(file_name, 'r') as file:
                for line in file:
                    text += line

            intr = Interpreter(text)
            print(intr.interpret())

        except TypeError as e:
            print(e)

        except KeyboardInterrupt:
            print("")
            return


if __name__ == "__main__":
    main()
