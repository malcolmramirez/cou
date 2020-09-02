from typing import List
from lang.tokenizer import Token
from lang.symtab import Symbol
import lang.token as tok

# Abstract syntax tree


class AST(object):
    """
    Superclass for AST nodes
    """

    def name(self) -> str:
        return "ast"

    def __repr__(self) -> str:
        return str(self)


class Number(AST):
    """
    Represents a number in the AST
    """

    def __init__(self, token: Token):
        self.value = token.value
        self.token = token

    def name(self) -> str:
        return "number"

    def __str__(self) -> str:
        return str(self.value)


class Boolean(AST):
    """
    Represents a boolean in the AST
    """

    def __init__(self, token: Token):
        self.value = token.value
        self.token = token

    def name(self) -> str:
        return "boolean"

    def __str__(self) -> str:
        return str(self.value)


class String(AST):
    """
    Represents a string in the AST
    """

    def __init__(self, token: Token):
        self.value = token.value
        self.token = token

    def name(self) -> str:
        return "string"

    def __str__(self) -> str:
        return self.value


class Nothing(AST):
    """
    Represents a nothing in the AST
    """

    def __init__(self, token: Token):
        self.value = None
        self.token = token

    def name(self) -> str:
        return "nothing"

    __str__ = name


class ArrayInitialization(AST):
    """
    Represents an array in the AST
    """

    def __init__(self, token: Token, size: AST):
        self.token = token
        self.size = size

    def name(self) -> str:
        return "array_initialization"

    def __str__(self) -> str:
        return f"arr {self.size}"


class ArrayElement(AST):
    """
    Represents an array element in the AST
    """

    def __init__(self, token: Token, indices: List[AST]):
        self.token = token
        self.arr_name = token.value
        self.indices = indices

    def name(self) -> str:
        return "array_element"

    def __str__(self) -> str:
        return f"{self.arr_name} {self.index}"

class ArrayElementAssignment(AST):
    """
    Represents an array element assignment in the AST
    """

    def __init__(self, left: AST, token: Token, right: AST):
        self.token = token
        self.left = left
        self.right = right

    def name(self) -> str:
        return "array_element_assignment"

    def __str__(self) -> str:
        return f"{self.arr_name} {self.left.index} = {self.right}"


class UnaryOperator(AST):
    """
    Represents a unary operator (eg, unary +/-, floor)
    """

    def __init__(self, token: Token, child: AST):
        self.value = token.type
        self.token = token
        self.child = child

    def name(self) -> str:
        return "unary_operator"

    def __str__(self) -> str:
        return f"{self.value}{self.child}"


class BinaryOperator(AST):
    """
    Represents a binary operator in the AST
    """

    def __init__(self, left: AST, token: Token, right: AST):
        self.left = left
        self.value = token.type
        self.token = token
        self.right = right

    def name(self) -> str:
        return "binary_operator"

    def __str__(self) -> str:
        return f"{self.left} {self.value} {self.right}"


class Variable(AST):
    """
    Represents a variable in the AST
    """

    def __init__(self, token: Token, var_type: str):
        self.value = token.value
        self.token = token
        self.var_type = var_type

    def name(self) -> str:
        return "variable"

    def __str__(self) -> str:
        return self.value


class VariableType(AST):

    def __init__(self, token: Token):
        self.value = token.value
        self.token = token

    def name(self) -> str:
        return "variable_type"

    def __str__(self) -> str:
        return self.value


class AssignmentStatement(AST):
    """
    Represents an assignment statement in the AST
    """

    def __init__(self, left: AST, token: Token, right: AST):
        self.left = left
        self.value = token.value
        self.token = token
        self.right = right

    def name(self) -> str:
        return "assignment_statement"

    def __str__(self) -> str:
        return f"{self.value} = {self.right}"


class Empty(AST):
    """
    Represents an empty statement in the AST
    """

    def __init__(self):
        self.value = None

    def name(self) -> str:
        return "empty"

    def __str__(self) -> str:
        return ";"


class VariableDeclaration(AST):
    """
    Represents a variable declaration
    """

    def __init__(self, variable: AST, variable_type: AST):
        self.variable = variable
        self.value = variable.value
        self.token = variable.token
        self.var_type = variable_type.value

    def name(self) -> str:
        return "variable_declaration"

    def __str__(self) -> str:
        return f"{self.variable}: {self.var_type}"


class Say(AST):
    """
    Represents something that is printed
    """

    def __init__(self, to_say: AST):
        self.value = to_say
        self.token = to_say.token

    def name(self) -> str:
        return "say"

    def __str__(self) -> str:
        return f"say {self.value}"


class Return(AST):
    """
    Represents a return statement
    """

    def __init__(self, statement: AST):
        self.statement = statement
        self.value = statement.value

    def name(self) -> str:
        return "return"

    def __str__(self) -> str:
        return f"return {self.value}"


class ProcessDeclaration(AST):
    """
    Represents a process declaration
    """

    def __init__(self, token: Token, type_def: AST, params: List[AST] = None):
        self.token = token
        self.value = token.value

        self.type_def = type_def.value
        self.params = params

    def name(self) -> str:
        return "process_declaration"

    def __str__(self) -> str:
        param_fmt = ''
        if self.params:
            param_fmt = str(self.params)
            param_fmt = param_fmt[1: len(param_fmt) - 1]

        return f"proc {self.token.value}: {self.type_def}({param_fmt})"


class ProcessCall(AST):

    def __init__(self, token: Token, args: List[AST], proc_sym: Symbol):
        self.value = token.value
        self.token = token
        self.args = args
        self.proc_sym = proc_sym

    def name(self) -> str:
        return "process_call"

    def __str__(self) -> str:
        args_fmt = str(self.args)
        return f"{self.value}({args_fmt[1 : len(args_fmt) - 1]})"


class Process(AST):
    """
    Represents a process
    """

    def __init__(self, declr: AST, block: AST):
        self.declr = declr
        self.token = declr.token
        self.value = declr.value
        self.block = block

    def name(self) -> str:
        return "process"

    def __str__(self) -> str:
        statement_fmt = ''
        if self.statements:
            statement_fmt = str(self.statements).replace(',', '    \n')
            statement_fmt = statement_fmt[1: len(statement_fmt) - 1]

        return f"{self.declr}{{ \n {statement_fmt}\n}}"


class Condition(AST):

    def __init__(self, condition: AST, block: AST):
        self.token = condition.token
        self.condition = condition
        self.block = block

    def name(self) -> str:
        return "condition"

    def __str__(self) -> str:
        return f"cond {self.condition} \n {self.block}"


class Conditions(AST):
    """
    Represents a block of conditions
    """

    def __init__(self, conditions: List[AST]):
        self.conditions = conditions

    def name(self) -> str:
        return "conditions"

    def __str__(self) -> str:
        return str(self.conditions)


class AsDeclaration(AST):

    def __init__(self, token: Token, counter: AST, condition: AST, after: AST):
        self.token = token
        self.counter = counter
        self.condition = condition
        self.after = after

    def name(self) -> str:
        return "as_declaration"

    def __str__(self) -> str:
        fmt = '('
        if self.var_declr:
            fmt += f"{self.var_declr};"
        fmt += f"{self.condition}"
        if self.asn_statement:
            fmt += f";{self.asn_statement}"
        fmt = ')'

        return fmt


class As(AST):
    """
    Represents an as loop
    """

    def __init__(self, token: Token, declr: AST, block: AST):
        self.token = token
        self.declr = declr
        self.block = block

    def name(self) -> str:
        return "as"

    def __str__(self) -> str:
        return f"as {self.declr} {self.block}"


class Block(AST):

    def __init__(self, statements: List[AST]):
        self.statements = statements

    def name(self) -> str:
        return "block"

    def __str__(self) -> str:
        statement_fmt = ''
        if self.statements:
            statement_fmt = str(self.statements).replace(',', '\n')
            statement_fmt = statement_fmt[1: len(statement_fmt) - 1]

        return statement_fmt


class Program(AST):
    """
    Represents a compound statement in the AST
    """

    def __init__(self, statements: List[AST] = None):
        self.statements = [] if not statements else statements

    def name(self) -> str:
        return "program"

    def __str__(self) -> str:
        statement_fmt = ''
        if self.statements:
            statement_fmt = str(self.statements).replace(',', '\n')
            statement_fmt = statement_fmt[1: len(statement_fmt) - 1]

        return statement_fmt
