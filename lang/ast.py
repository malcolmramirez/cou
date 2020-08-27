from lang.tokenizer import Token

# Abstract syntax tree


class AST(object):
    """
    Superclass for AST nodes
    """

    def name(self) -> str:
        return "ast"


class Number(AST):
    """
    Represents a number in the AST
    """

    def __init__(self, token: Token):
        self.value = token.value

    def name(self) -> str:
        return "number"


class Boolean(AST):
    """
    Represents a boolean in the AST
    """

    def __init__(self, token: Token):
        self.value = token.value

    def name(self) -> str:
        return "boolean"


class String(AST):
    """
    Represents a string in the AST
    """

    def __init__(self, token: Token):
        self.value = token.value

    def name(self) -> str:
        return "string"


class UnaryOperator(AST):
    """
    Represents a unary operator (eg, unary +/-, floor)
    """

    def __init__(self, token: Token, child: AST):
        self.value = token.type
        self.child = child

    def name(self) -> str:
        return "unary_operator"


class BinaryOperator(AST):
    """
    Represents a binary operator in the AST
    """

    def __init__(self, left: AST, token: Token, right: AST):
        self.left = left
        self.value = token.type
        self.right = right

    def name(self) -> str:
        return "binary_operator"


class Variable(AST):
    """
    Represents a variable in the AST
    """

    def __init__(self, token: Token):
        self.value = token.value

    def name(self) -> str:
        return "variable"


class VariableType(AST):

    def __init__(self, token: Token):
        self.value = token.value

    def name(self) -> str:
        return "variable_type"


class AssignmentStatement(AST):
    """
    Represents an assignment statement in the AST
    """

    def __init__(self, left: AST, token: Token, right: AST):
        self.left = left
        self.value = token.value
        self.right = right

    def name(self) -> str:
        return "assignment_statement"


class Empty(AST):
    """
    Represents an empty statement in the AST
    """

    def name(self) -> str:
        return "empty"


class VariableDeclaration(AST):
    """
    Represents a variable declaration
    """

    def __init__(self, variable: AST, variable_type: AST):
        self.variable = variable
        self.value = variable.value
        self.variable_type = variable_type

    def name(self) -> str:
        return "variable_declaration"


class Say(AST):
    """
    Represents something that is printed
    """

    def __init__(self, to_say: AST):
        self.value = to_say

    def name(self) -> str:
        return "say"


class Program(AST):
    """
    Represents a compound statement in the AST
    """

    def __init__(self, statements: list = None):
        self.statements = [] if not statements else statements

    def name(self) -> str:
        return "program"
