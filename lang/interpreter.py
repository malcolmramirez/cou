import lang.tokens as tkns

from lang.lexer import Token, Lexer
from lang.parser import Parser
from lang.ast import AST

from collections import defaultdict

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

        return getattr(self, node.name(), self.visit_error)(node)

    def visit_error(self, node: AST):
        """
        Raises error if no visit method for a node type
        """

        raise ValueError("No visit method for node type: {}", node.name())


class Interpreter(Visitor):
    """
    Evaluates expressions from the parser
    """

    def __init__(self, text: str = None):
        """
        Initializes interpreter with a parser, used to eval. expressions
        """

        self.global_scope = defaultdict()

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

        if type == tkns.ROUND:
            return round(self.visit(node.child))

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

        id = node.id()

        if id not in self.global_scope:
            raise NameError("Variable \"" + id +
                            "\" referenced before assignment")

        return self.global_scope[id]

    def say(self, node: AST) -> None:
        """
        Interprets a say statement
        """

        visited = self.visit(node.to_say)

        print(str(visited))

    def assignment_statement(self, node: AST) -> None:
        """
        Interprets an assignment statement
        """

        var = node.left.id()
        self.global_scope[var] = self.visit(node.right)

    def program(self, node: AST) -> None:
        """
        Interprets a program
        """

        for child in node.statements:
            self.visit(child)

    def empty(self, node: AST) -> None:
        """
        Interprets an empty expression
        """

        return

    def interpret(self, text: str) -> str:
        """
        Interprets a line of text.
        """

        parser = Parser(Lexer(text))
        self.visit(parser.parse())
