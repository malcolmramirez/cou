import lang.tokens as tkns
import lang.typeutils as typeutils

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

        var_name = node.value

        if not self.table.exists(var_name):
            raise NameError(
                "Variable \"{}\" referenced before declaration".format(var_name))

    def variable_declaration(self, node: AST) -> None:
        """
        Visits a variable_declaration
        """

        var_name = node.value
        var_type = node.variable_type.value

        if self.table.exists(var_name):
            raise NameError(
                "Variable \"{}\" declared more than once".format(var_name))

        type_sym = TypeSymbol(var_type)
        var_sym = VariableSymbol(var_name, type_sym)

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

    def __init__(self, text: str):
        """
        Initializes interpreter with a parser, used to eval. expressions
        """

        parser = Parser(Lexer(text))
        builder = SymbolTableBuilder()

        self.tree = parser.parse()
        self.symbol_table = builder.construct(self.tree)
        self.global_memory = {}

    def number(self, node: AST) -> int:
        """
        Visits a number node (just needs to return the value)
        """

        return node.value

    def boolean(self, node: AST) -> bool:
        """
        Visits a boolean node (just needs to return the value)
        """

        return node.value

    def string(self, node: AST) -> bool:
        """
        Visits a boolean node (just needs to return the value)
        """

        return node.value

    def unary_operator(self, node: AST) -> int:
        """
        Visits a unary operator (can be +/-/~)
        """

        type = node.value

        if type == tkns.ADD:
            return self.visit(node.child)

        if type == tkns.SUB:
            return -self.visit(node.child)

        raise SyntaxError("Invalid operator \"{}\"".format(node.value))

    def binary_operator(self, node: AST) -> int:
        """
        Visits a binary operator node on the AST (will recur until a number is
        retrieved)
        """

        op_type = node.value

        if op_type == tkns.ADD:
            return self.visit(node.left) + self.visit(node.right)

        if op_type == tkns.SUB:
            return self.visit(node.left) - self.visit(node.right)

        if op_type == tkns.MUL:
            return self.visit(node.left) * self.visit(node.right)

        if op_type == tkns.DIV:
            return self.visit(node.left) / self.visit(node.right)

        if op_type == tkns.I_DIV:
            return self.visit(node.left) // self.visit(node.right)

        raise SyntaxError("Invalid operator \"{}\"".format(node.value))

    def variable(self, node: AST) -> AST:
        """
        Interprets a variable
        """

        return self.global_memory[node.value]

    def variable_declaration(self, node: AST) -> None:
        """
        Interprets a variable declaration
        """

        self.global_memory[node.value] = None

    def say(self, node: AST) -> None:
        """
        Interprets a say statement
        """

        visited = self.visit(node.value)
        print(str(visited))

    def assignment_statement(self, node: AST) -> None:
        """
        Interprets an assignment statement
        """

        var_id = node.left.value
        asn = self.visit(node.right)

        cou_type = self.symbol_table.get(var_id).type_name

        if not typeutils.is_assignable(cou_type, asn):
            raise SyntaxError("Cannot assign '{}' to type '{}'".format(asn, cou_type))

        self.global_memory[var_id] = assigned

    def program(self, node: AST) -> None:
        """
        Interprets a program
        """

        for child in node.statements:
            self.visit(child)

    def interpret(self) -> None:
        """
        Interprets a line of text.
        """

        self.visit(self.tree)
