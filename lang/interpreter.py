
from typing import Any

import lang.token as tok
import lang.validation as validation

from lang.error import error
from lang.tokenizer import Token, Tokenizer
from lang.parser import Parser
from lang.ast import AST
from lang.callstack import CallStack, ActivationRecord

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


class Interpreter(Visitor):
    """
    Evaluates expressions from the parser
    """

    def __init__(self, text: str):
        """
        Initializes interpreter with a parser, used to eval. expressions
        """

        self.parser = Parser(Tokenizer(text))
        self.stack = CallStack()

    def _number(self, node: AST) -> int:
        """
        Visits a number node (just needs to return the value)
        """

        return node.value

    def _boolean(self, node: AST) -> bool:
        """
        Visits a boolean node (just needs to return the value)
        """

        return node.value == 'true'

    def _string(self, node: AST) -> str:
        """
        Visits a string node (just needs to return the value)
        """

        return node.value

    def _nothing(self, node: AST) -> None:
        """
        Visits a nothing node
        """

        return None

    def _unary_operator(self, node: AST) -> Any:
        """
        Visits a unary operator (can be +/-)
        """

        op_type = node.value
        token = node.token

        operand = self.visit(node.child)
        validation.validate_operation(op_type, token, operand)

        if op_type == tok.NOT:
            return not operand

        if op_type == tok.ADD:
            return operand

        if op_type == tok.SUB:
            return -operand

        token = node.token
        error(f"Invalid unary operator {op_type}", token)

    def _binary_operator(self, node: AST) -> Any:
        """
        Visits a binary operator node on the AST (will recur until a number is
        retrieved)
        """

        op_type = node.value

        l = self.visit(node.left)
        r = self.visit(node.right)

        token = node.token
        validation.validate_operation(op_type, token, l, r)

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

        error(f"Invalid binary operator '{op_type}'", token)

    def _variable(self, node: AST) -> AST:
        """
        Interprets a variable
        """

        record = self.stack.peek()
        return record[node.value]

    def _variable_declaration(self, node: AST) -> None:
        """
        Interprets a variable declaration
        """

        fr = self.stack.peek()
        fr[node.value] = None

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
        var_type = node.left.var_type
        token = node.token

        asn = self.visit(node.right)
        validation.validate_type(var_type, token, asn)

        record = self.stack.peek()
        record[var_id] = asn

    def _conditional_if(self, node: AST) -> None:
        """
        Interprets a conditional if
        """

        token = node.token

        cond_result = self.visit(node.condition)
        validation.validate_condition(token, cond_result)

        if cond_result:
            self.visit(node.block)

    def _return(self, node: AST) -> None:
        """
        Interprets a return statement
        """

        fr = self.stack.peek()
        ret_val = self.visit(node.statement)

        fr.ret_val = ret_val
        fr.returned = True

    def _process_call(self, node: AST) -> Any:
        """
        Interprets a process call
        """

        proc_name = node.value
        proc_sym = node.proc_sym

        record = ActivationRecord(proc_name, proc_sym.sc_level, self.stack.peek())

        for param, arg in zip(proc_sym.params, node.args):
            record[param.value] = self.visit(arg)

        self.stack.push(record)
        self.visit(proc_sym.process.block)

        ret_val = self.stack.pop()
        validation.validate_return(proc_sym.type_def, node.token, ret_val)

        return ret_val

    def _block(self, node: AST) -> None:
        """
        Interprets a block of code
        """

        record = self.stack.peek()
        for statement in node.statements:
            self.visit(statement)
            if record.returned:
                return # Return when we hit a ret statement

    def _program(self, node: AST) -> None:
        """
        Interprets a program
        """

        record = ActivationRecord("main", 1)
        self.stack.push(record)

        for statement in node.statements:
            self.visit(statement)

        self.stack.pop()

    def interpret(self) -> None:
        """
        Interprets a line of text.
        """

        self.visit(self.parser.parse())
