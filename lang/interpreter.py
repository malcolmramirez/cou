import lang.tokens as tkns

from lang.lexer import Token, Lexer
from lang.parser import Parser
from lang.ast import AST
from lang.symbol import SymbolTable, TypeSymbol, VariableSymbol

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

        return getattr(self, node.name(), self.default)(node)

    def default(self, node: AST):
        """
        Does nothing, default response for nodes
        """

        return


class SymbolTableBuilder(Visitor):
    """
    Builds symbol table for interpreter
    """

    def __init__(self):
        self.table = SymbolTable()

    def variable(self, node: AST) -> None:
        """
        Visits a variable
        """

        name = node.value()

        if not self.table.exists(name):
            raise NameError(
                "Variable \"{}\" referenced before declaration".format(name))

    def variable_declaration(self, node: AST) -> None:
        """
        Visits a variable_declaration
        """

        name = node.value()
        type = node.type.value()

        if self.table.exists(name):
            raise NameError(
                "Variable \"{}\" declared more than once".format(name))

        type_sym = TypeSymbol(type)
        var_sym = VariableSymbol(name, type_sym)

        self.table.put(var_sym)

    def unary_operator(self, node: AST) -> None:
        """
        Visits a unary operator
        """

        self.visit(node.child)

    def binary_operator(self, node: AST) -> None:
        """
        Visits a binary operator
        """

        self.visit(node.left)
        self.visit(node.right)

    def assignment_statement(self, node: AST) -> None:
        """
        Visits an assignment statement
        """

        self.visit(node.left)
        self.visit(node.right)

    def program(self, node: AST) -> None:
        """
        Visits a program
        """

        for statement in node.statements:
            self.visit(statement)

    def construct(self, tree: AST) -> SymbolTable:
        """
        Constructs a symbol table given an ast
        """

        self.visit(tree)

        return self.table


class Interpreter(Visitor):
    """
    Evaluates expressions from the parser
    """

    def __init__(self):
        """
        Initializes interpreter with a parser, used to eval. expressions
        """

        self.global_memory = {}

    def number(self, node: AST) -> int:
        """
        Visits a number node (just needs to return the value)
        """

        return node.value()

    def boolean(self, node: AST) -> bool:
        """
        Visits a boolean node (just needs to return the value)
        """

        return node.value()

    def string(self, node: AST) -> bool:
        """
        Visits a boolean node (just needs to return the value)
        """

        return node.value()

    def unary_operator(self, node: AST) -> int:
        """
        Visits a unary operator (can be +/-/~)
        """

        type = node.type()

        if type == tkns.ADD:
            return self.visit(node.child)

        if type == tkns.SUB:
            return -self.visit(node.child)

        raise SyntaxError("Invalid operator \"{}\"".format(node.value()))

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

        raise SyntaxError("Invalid numeric operator \"{}\"".format(node.value()))

    def variable(self, node: AST) -> AST:
        """
        Interprets a variable
        """

        var = node.value()
        return self.global_memory[var]

    def variable_declaration(self, node: AST) -> None:
        """
        Interprets a variable declaration
        """

        var = node.value()
        self.global_memory[var] = None

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

        var = node.left.value()
        self.global_memory[var] = self.visit(node.right)

    def program(self, node: AST) -> None:
        """
        Interprets a program
        """

        for child in node.statements:
            self.visit(child)

    def interpret(self, text: str) -> str:
        """
        Interprets a line of text.
        """

        parser = Parser(Lexer(text))
        tree = parser.parse()

        builder = SymbolTableBuilder()
        symbol_table = builder.construct(tree)

        self.visit(tree)
