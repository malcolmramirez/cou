
import lang.token as tok

from typing import Any

from lang.tokenizer import Token, Tokenizer
from lang.parser import Parser
from lang.ast import AST
from lang.symbol import SymbolTable, VariableSymbol
from lang.type import valid_type, valid_operation

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

        return getattr(self, f"_{node.name()}", self.default)(node)

    def default(self, node: AST):
        """
        Does nothing, default response for nodes
        """

        return


class SymbolTableBuilder(Visitor):
    """
    Builds symbol table for interpreter
    """

    def __init__(self, tree: AST):
        self.tree = tree
        self.table = SymbolTable()

    def _variable(self, node: AST) -> None:
        """
        Visits a variable
        """

        var_name = node.value

        if not self.table.exists(var_name):
            raise NameError(
                f"Variable '{var_name}' referenced before declaration")

    def _variable_declaration(self, node: AST) -> None:
        """
        Visits a variable_declaration
        """

        var_name = node.value
        var_type = node.variable_type.value

        if self.table.exists(var_name):
            raise NameError(f"Variable '{var_name}' declared more than once")

        var_sym = VariableSymbol(var_name, var_type)

        self.table.put(var_sym)

    def _unary_operator(self, node: AST) -> None:
        """
        Visits a unary operator
        """

        self.visit(node.child)

    def _binary_operator(self, node: AST) -> None:
        """
        Visits a binary operator
        """

        self.visit(node.left)
        self.visit(node.right)

    def _assignment_statement(self, node: AST) -> None:
        """
        Visits an assignment statement
        """

        self.visit(node.left)
        self.visit(node.right)

    def _program(self, node: AST) -> None:
        """
        Visits a program
        """

        for statement in node.statements:
            self.visit(statement)

    def construct(self) -> SymbolTable:
        """
        Constructs a symbol table given an ast
        """

        self.visit(self.tree)

        return self.table


class Interpreter(Visitor):
    """
    Evaluates expressions from the parser
    """

    def __init__(self, text: str):
        """
        Initializes interpreter with a parser, used to eval. expressions
        """

        parser = Parser(Tokenizer(text))

        self.tree = parser.parse()
        self.symbol_table = SymbolTableBuilder(self.tree).construct()

        self.global_memory = {}

    def _number(self, node: AST) -> int:
        """
        Visits a number node (just needs to return the value)
        """

        return node.value

    def _boolean(self, node: AST) -> bool:
        """
        Visits a boolean node (just needs to return the value)
        """

        return node.value

    def _string(self, node: AST) -> str:
        """
        Visits a string node (just needs to return the value)
        """

        return node.value

    def _unary_operator(self, node: AST) -> Any:
        """
        Visits a unary operator (can be +/-)
        """

        op_type = node.value
        operand = self.visit(node.child)

        if not valid_operation(op_type, operand):
            raise SyntaxError(f"Invalid operator '{node.value}' for operand {operand}")

        if op_type == tok.NOT:
            return not operand

        if op_type == tok.ADD:
            return operand

        if op_type == tok.SUB:
            return -operand

        raise SyntaxError(f"Invalid unary operator {op_type}")


    def _binary_operator(self, node: AST) -> Any:
        """
        Visits a binary operator node on the AST (will recur until a number is
        retrieved)
        """

        op_type = node.value

        l = self.visit(node.left)
        r = self.visit(node.right)

        if not valid_operation(op_type, l, r):
            raise SyntaxError(
                f"Invalid operation \'{op_type}\' between \'{l}\', \'{r}\'")

        if op_type == tok.ADD:
            return l + r

        if op_type == tok.SUB:
            return l - r

        if op_type == tok.MUL:
            return l * r

        if op_type == tok.DIV:
            return l / r

        if op_type == tok.I_DIV:
            return l // r

        if op_type == tok.OR:
            return l or r

        if op_type == tok.AND:
            return l and r

        if op_type == tok.EQ:
            return l == r

        if op_type == tok.NEQ:
            return l != r

        if op_type == tok.GREATER:
            return l > r

        if op_type == tok.GEQ:
            return l >= r

        if op_type == tok.LESS:
            return l < r

        if op_type == tok.LEQ:
            return l <= r

        raise SyntaxError(f"Invalid binary operator '{op_type.value}'")

    def _variable(self, node: AST) -> AST:
        """
        Interprets a variable
        """

        return self.global_memory[node.value]

    def _variable_declaration(self, node: AST) -> None:
        """
        Interprets a variable declaration
        """

        self.global_memory[node.value] = None

    def _say(self, node: AST) -> None:
        """
        Interprets a say statement
        """

        visited = self.visit(node.value)
        repr = str(visited)

        if isinstance(visited, bool):
            # Make it so that the string representation of booleans begin lower
            repr = repr.lower()

        print(repr)

    def _assignment_statement(self, node: AST) -> None:
        """
        Interprets an assignment statement
        """

        var_id = node.left.value
        asn = self.visit(node.right)

        var_type = self.symbol_table.get(var_id).type_def
        if not valid_type(var_type, asn):
            raise SyntaxError(f"Cannot assign \'{asn}\' to \'{var_type}\'")

        if var_type == tok.REAL and type(asn) == int:
            asn = float(asn)

        self.global_memory[var_id] = asn

    def _program(self, node: AST) -> None:
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
