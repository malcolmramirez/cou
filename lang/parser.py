
import lang.token as tok
from lang.tokenizer import Tokenizer
from lang.ast import *

# Parser

class Parser:
    """
    Parses tokens into an AST to be used by the interpreter.
    """

    def __init__(self, tokenizer: Tokenizer):
        """
        Initializes parser with a tokenizer and a current token
        """

        self._tokenizer = tokenizer
        self.curr = self._tokenizer.produce()

    def _consume(self, type) -> None:
        """
        Consumes a token of the specified type, raising an error if the current
        token in the stream is not that type.
        """

        if self.curr.type != type:
            raise SyntaxError(f"Expected '{type}'")

        self.curr = self._tokenizer.produce()

    def _operand(self) -> AST:
        """
        Parses an operand
            operand : number | bool | string | (expression) | (add|sub|round) operand | variable
        """

        operand_token = self.curr
        node = None

        if operand_token.type == tok.NUMBER:
            self._consume(operand_token.type)
            node = Number(operand_token)

        elif operand_token.type == tok.STRING:
            self._consume(operand_token.type)
            node = String(operand_token)

        elif operand_token.type == tok.BOOLEAN:
            self._consume(operand_token.type)
            node = Boolean(operand_token)

        elif operand_token.type == tok.ID:
            self._consume(tok.ID)
            node = Variable(operand_token)

        elif operand_token.type in (tok.ADD, tok.SUB, tok.NOT):
            self._consume(operand_token.type)
            node = UnaryOperator(operand_token, self._operand())

        elif operand_token.type == tok.L_PAREN:
            self._consume(tok.L_PAREN)
            node = self._expression()
            self._consume(tok.R_PAREN)

        else:
            raise SyntaxError(f"Unexpected operand {operand_token.value}")

        return node

    def _term(self) -> AST:
        """
        Parses a term
            term : operand ((mul|div|and) operand)*
        """

        node = self._operand()
        operator = self.curr

        while operator.type in (tok.MUL, tok.DIV, tok.I_DIV, tok.AND):
            self._consume(operator.type)
            node = BinaryOperator(node, operator, self._operand())
            operator = self.curr

        return node

    def _expression(self) -> AST:
        """
        Parses an expression
            term : term ((add|sub|or) term)*
        """

        node = self._term()
        operator = self.curr

        while operator.type in (tok.ADD, tok.SUB, tok.OR):
            self._consume(operator.type)
            node = BinaryOperator(node, operator, self._term())
            operator = self.curr

        return node

    def _comparison(self) -> AST:
        """
        Parses a comparison (==, !=, <=, >=, <, >)
            comparison = expression [ == | != | <= | >= | < | > ] expression
        """

        node = self._expression()
        operator = self.curr

        while operator.type in (tok.EQ, tok.NEQ, tok.GEQ, tok.LEQ, tok.GREATER, tok.LESS):
            self._consume(operator.type)
            node = BinaryOperator(node, operator, self._expression())
            operator = self.curr

        return node



    def _string(self) -> AST:
        """
        Parses a string
            string : quote char* quote
        """

        token = self.curr
        self._consume(tok.STRING)

        return String(token)

    def _variable(self) -> AST:
        """
        Parses a variable
            variable : ID
        """

        token = self.curr
        self._consume(tok.ID)

        return Variable(token)

    def _variable_type(self) -> AST:
        """
        Parses a type
            type : int | real | bool | str
        """

        token = self.curr

        if token.type == tok.INT:
            self._consume(tok.INT)

        elif token.type == tok.REAL:
            self._consume(tok.REAL)

        elif token.type == tok.BOOL:
            self._consume(tok.BOOL)

        elif token.type == tok.STR:
            self._consume(tok.STR)

        else:
            raise SyntaxError(f"invalid type {token.type}")

        return VariableType(token)

    def _say(self) -> AST:
        """
        Parses a say function
            say : say expression
        """

        self._consume(tok.SAY)
        node = self._expression()

        return Say(node)

    def _empty(self) -> AST:
        """
        Parses an empty expression:
            empty :
        """

        return Empty()

    def _assignment_statement(self) -> AST:
        """
        Parses an assignment statement
            statement : variable assign expression
                            | variable_declaration assign expression
        """

        to_assign = self._variable()
        token = self.curr

        if token.type == tok.COLON:
            self._consume(tok.COLON)
            to_assign = VariableDeclaration(to_assign, self._variable_type())

        self._consume(tok.ASSIGN)
        assigned = self._expression()

        return AssignmentStatement(to_assign, token, assigned)

    def _statement(self) -> AST:
        """
        Parses a statement
            statement : [ empty | assignment_statement | say | operand ] sep
        """

        token = self.curr

        if token.type == tok.ID:
            stmt = self._assignment_statement()

        elif token.type == tok.SAY:
            stmt = self._say()

        else:
            stmt = self._empty()

        self._consume(tok.SEP)

        return stmt

    def _program(self) -> AST:
        """
        Parses a program
            program : statement* eof
        """

        statements = []
        while self.curr.type != tok.EOF:
            statements.append(self._statement())

        self._consume(tok.EOF)

        return Program(statements)

    def parse(self) -> AST:
        """
        Parses all valid expressions in grammar
        """

        return self._program()
