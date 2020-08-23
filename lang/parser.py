import lang.tokens as tkns

from lang.lexer import Lexer
from lang.ast import *

# Parser

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

    def syntax_error(self, syntax: str):
        """
        Raises syntax error
        """

        raise SyntaxError("Invalid syntax \"" + str(syntax) + "\"")

    def consume(self, type: str) -> None:
        """
        Consumes a token of the specified type, raising an error if the current
        token in the stream is not that type.
        """

        if self.curr.type != type:
            raise SyntaxError("Expected '{}'".format(type))

        self.curr = self.lexer.token()

    def operand(self) -> AST:
        """
        Parses an operand
            operand : number | bool | string | (expression) | (add|sub|round) operand | variable
        """

        operand_token = self.curr
        node = None

        if operand_token.type in (tkns.INT_CONST, tkns.REAL_CONST):
            self.consume(operand_token.type)
            node = Number(operand_token)

        elif operand_token.type in (tkns.BOOL_T, tkns.BOOL_F):
            self.consume(operand_token.type)
            node = Boolean(operand_token)

        elif operand_token.type == tkns.STR_CONST:
            self.consume(operand_token.type)
            node = String(operand_token)

        elif operand_token.type == tkns.ID:
            self.consume(tkns.ID)
            node = Variable(operand_token)

        elif operand_token.type in (tkns.ADD, tkns.SUB, tkns.NOT):
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

    def string(self) -> AST:
        """
        Parses a string
            string : quote char* quote
        """

        token = self.curr
        self.consume(tkns.T_STR)

        return String(token)

    def variable(self) -> AST:
        """
        Parses a variable
            variable : ID
        """

        token = self.curr
        self.consume(tkns.ID)

        return Variable(token)

    def variable_type(self) -> AST:
        """
        Parses a type
            type : int | real | bool | str
        """

        token = self.curr
        self.consume(tkns.TYPE)

        return VariableType(token)

    def say(self) -> AST:
        """
        Parses a say function
            say : say expression
        """

        self.consume(tkns.SAY)
        node = self.expression()

        return Say(node)

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
                            | variable_declaration assign expression
        """

        to_assign = self.variable()
        token = self.curr

        if token.type == tkns.COLON:
            self.consume(tkns.COLON)
            to_assign = VariableDeclaration(to_assign, self.variable_type())

        self.consume(tkns.ASSIGN)

        return AssignmentStatement(to_assign, token, self.expression())

    def statement(self) -> AST:
        """
        Parses a statement
            statement : [ empty | assignment_statement | say | operand ] sep
        """

        token = self.curr

        if token.type == tkns.ID:
            stmt = self.assignment_statement()

        elif token.type == tkns.SAY:
            stmt = self.say()

        else:
            stmt = self.empty()

        self.consume(tkns.SEP)

        return stmt

    def program(self) -> AST:
        """
        Parses a program
            program : statement* eof
        """

        statements = []
        while self.curr.type != tkns.EOF:
            statements.append(self.statement())

        self.consume(tkns.EOF)

        return Program(statements)

    def parse(self) -> AST:
        """
        Parses all valid expressions in grammar
        """

        return self.program()
