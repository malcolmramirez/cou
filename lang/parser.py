import tokens as tkns

from lexer import Token, Lexer

# Parser

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
        self.token = token


    def value(self) -> int:
        return self.token.value


    def name(self) -> str:
        return "number"


class UnaryOperator(AST):
    """
    Represents a unary operator (eg, unary +/-, floor)
    """

    def __init__(self, token: Token, child: AST):
        self.token = token
        self.child = child


    def type(self) -> str:
        return self.token.type


    def name(self) -> str:
        return "unary_operator"


class BinaryOperator(AST):
    """
    Represents a binary operator in the AST
    """

    def __init__(self, left: AST, token: Token, right: AST):
        self.left = left
        self.token = token
        self.right = right


    def type(self) -> str:
        return self.token.type


    def name(self) -> str:
        return "binary_operator"


class Variable(AST):
    """
    Represents a variable in the AST
    """

    def __init__(self, token: Token):
        self.token = token


    def sym(self) -> str:
        return self.token.value


    def name(self) -> str:
        return "variable"


class CompoundStatement(AST):
    """
    Represents a compound statement in the AST
    """

    def __init__(self, children: list = None):
        self.children = [] if not children else children


    def name(self) -> str:
        return "compound_statement"


class AssignmentStatement(AST):
    """
    Represents an assignment statement in the AST
    """

    def __init__(self, left: AST, token: Token, right: AST):
        self.left = left
        self.token = token
        self.right = right


    def name(self) -> str:
        return "assignment_statement"


class Empty(AST):
    """
    Represents an empty statement in the AST
    """

    def name(self) -> str:
        return "empty"


class Parser:
    """
    Parses tokens into an AST to be used by the interpreter.
    """

    def __init__(self, lexer: Lexer):
        """
        Initializes parser with a lexer and a current token
        """

        self.lexer = lexer
        self.curr = self.lexer.token()


    def syntax_error(self, syntax):
        """
        Raises syntax error
        """

        raise TypeError("Invalid syntax \"" + str(syntax) + "\"")


    def consume(self, type: str) -> None:
        """
        Consumes a token of the specified type, raising an error if the current
        token in the stream is not that type.
        """

        if self.curr.type != type:
            self.syntax_error(self.curr.value)

        self.curr = self.lexer.token()


    def operand(self) -> AST:
        """
        Parses an operand
            operand : int | real | (expression) | (add|sub|floor) operand
        """

        operand_token = self.curr
        node = None

        if operand_token.type in (tkns.INT, tkns.REAL):
            self.consume(operand_token.type)
            node = Number(operand_token)

        elif operand_token.type == tkns.ID:
            self.consume(tkns.ID)
            node = Variable(operand_token)

        elif operand_token.type in (tkns.ADD, tkns.SUB, tkns.FLOOR):
            self.consume(operand_token.type)
            node = UnaryOperator(operand_token, self.operand())

        elif operand_token.type == tkns.L_PAREN:
            self.consume(tkns.L_PAREN)
            node = self.expression()
            self.consume(tkns.R_PAREN)

        else:
            self.syntax_error(operand_token.value)

        return node


    def term(self) -> AST:
        """
        Parses a term
            term : operand ((mul|div) operand)*
        """

        node = self.operand()
        operator = self.curr

        while operator.type in (tkns.MUL, tkns.DIV, tkns.I_DIV):

            self.consume(operator.type)

            node = BinaryOperator(node, operator, self.operand())
            operator = self.curr

        return node


    def expression(self) -> AST:
        """
        Parses an expression
            term : term ((add|sub) term)*
        """

        node = self.term()
        operator = self.curr

        while operator.type in (tkns.ADD, tkns.SUB):

            self.consume(operator.type)

            node = BinaryOperator(node, operator, self.term())
            operator = self.curr

        return node


    def variable(self) -> AST:
        """
        Parses a variable
            variable : ID
        """

        token = self.curr
        self.consume(tkns.ID)

        return Variable(token)


    def empty(self) -> AST:
        """
        Parses an empty expression:
            empty :
        """

        return Empty()


    def assignment_statement(self) -> AST:
        """
        Parses an assignment statement
            statement : variable assign expression
        """

        var = self.variable()
        token = self.curr

        self.consume(tkns.ASSIGN)
        stmt = AssignmentStatement(var, token, self.expression())

        return stmt


    def statement(self) -> AST:
        """
        Parses a statement
            statement : compound_statement | empty | assignment_statement sep
        """

        token = self.curr

        if token.type == tkns.ID:
            stmt = self.assignment_statement()
            self.consume(tkns.SEP)

        elif token.type == tkns.START:
            stmt = self.compound_statement()

        else:
            stmt = self.empty()

        return stmt


    def compound_statement(self) -> AST:
        """
        Parses a compound statement
            compound_statement : BEG statements END
        """

        self.consume(tkns.START)

        children = []
        while self.curr.type != tkns.END:
            children.append(self.statement())

        self.consume(tkns.END)

        return CompoundStatement(children)


    def program(self) -> AST:
        """
        Parses a program
            program : compound_statement eof
        """

        ast = self.compound_statement()
        self.consume(tkns.EOF)

        return ast


    def parse(self) -> AST:
        """
        Parses all valid expressions in grammar
        """

        return self.program()
