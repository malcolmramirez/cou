
from typing import Any, List

import lang.token as tok
import lang.validation as validation

from lang.error import error
from lang.tokenizer import Token, Tokenizer
from lang.parser import Parser
from lang.ast import AST
from lang.callstack import CallStack, ActivationRecord, Record

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

    def _cou_str(self, conv: Any) -> str:
        """
        Utility function to convert to string
        """

        s_conv = str(conv)

        if isinstance(conv, list):
            n = len(conv)
            s_conv = '['

            for i, elem in enumerate(conv):
                s_conv += f"{self._cou_str(elem)}"
                if i < n - 1:
                    s_conv += ', '
            s_conv += ']'

        elif isinstance(conv, bool):
            # Make it so that the string representation of booleans begin lower
            s_conv = s_conv.lower()

        elif isinstance(conv, type(None)):
            # None -> nothing
            s_conv = 'nothing'

        return s_conv

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

    def _array_element(self, node: AST) -> Any:
        """
        Visits an array element
        """

        token = node.token

        record = self.stack.peek()
        arr = record[node.arr_name]

        indices = node.indices
        asn_i = len(indices) - 1

        for i in range(asn_i):
            index = self.visit(indices[i])
            validation.validate_array_index(token, index, arr)

            arr = arr[index]

        index = self.visit(indices[asn_i])
        validation.validate_array_index(token, index, arr)
        return arr[index]

    def _array_element_assignment(self, node: AST) -> None:
        """
        Visits an array element assignment
        """

        token = node.token

        record = self.stack.peek()
        arr = record[node.left.arr_name]

        indices = node.left.indices
        asn_i = len(indices) - 1

        for i in range(asn_i):
            index = self.visit(indices[i])
            validation.validate_array_index(token, index, arr)

            arr = arr[index]

        index = self.visit(indices[asn_i])
        validation.validate_array_index(token, index, arr)
        arr[index] = self.visit(node.right)


    def _array_initialization(self, node: AST) -> None:
        """
        Visits an array assignment
        """

        size = self.visit(node.size)
        validation.validate_array_size(node.token, size)

        return [None] * size

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

            if type(l) == str:
                r = self._cou_str(r)

            elif type(r) == str:
                l = self._cou_str(l)

            return l + r

        if op_type == tok.SUB:
            return l - r

        if op_type == tok.MUL:
            return l * r

        if op_type == tok.DIV:
            return l / r

        if op_type == tok.MOD:
            return l % r

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

        record = self.stack.peek()
        record[node.value] = None

    def _say(self, node: AST) -> None:
        """
        Interprets a say statement
        """

        visited = self.visit(node.value)
        print(self._cou_str(visited))

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

    def _conditions(self, node: AST) -> None:
        """
        Interprets a conditional block
        """

        for cond in node.conditions:

            eval = self.visit(cond.condition)
            validation.validate_condition(cond.token, eval)

            if eval:
                self.visit(cond.block)
                return

    def _as(self, node: AST) -> None:
        """
        Interprets an as loop
        """

        counter = node.declr.counter
        condition = node.declr.condition
        do_after = node.declr.after

        if counter:
            self.visit(counter)

        condition_eval = self.visit(condition)
        validation.validate_condition(node.token, condition_eval)

        while condition_eval:
            self.visit(node.block)
            if do_after:
                self.visit(do_after)

            condition_eval = self.visit(condition)
            validation.validate_condition(node.token, condition_eval)


    def _return(self, node: AST) -> None:
        """
        Interprets a return statement
        """

        record = self.stack.peek()
        ret_val = self.visit(node.statement)

        record.ret_val = ret_val
        record.returned = True

    def _process_call(self, node: AST) -> Any:
        """
        Interprets a process call
        """

        proc_name = node.value
        proc_sym = node.proc_sym

        record = ActivationRecord(
            proc_name, proc_sym.sc_level, self.stack.peek())

        for param, arg in zip(proc_sym.params, node.args):
            record[param.value] = self.visit(arg)

        self.stack.push(record)
        self.visit(proc_sym.process.block)

        ret_val = self.stack.pop().ret_val
        validation.validate_return(proc_sym.type_def, node.token, ret_val)

        return ret_val

    def _execute_statements(self, statements: List[AST]) -> None:
        """
        Executes a list of statements until a return or end of block is hit
        """

        record = self.stack.peek()

        for statement in statements:
            self.visit(statement)
            if record.returned:
                return  # Return when we hit a ret statement

    def _block(self, node: AST) -> None:
        """
        Interprets a block of code
        """

        self._execute_statements(node.statements)

    def _program(self, node: AST) -> None:
        """
        Interprets a program
        """

        record = ActivationRecord("main", 1)
        self.stack.push(record)

        self._execute_statements(node.statements)

        self.stack.pop()

    def interpret(self) -> None:
        """
        Interprets a line of text.
        """

        self.visit(self.parser.parse())
