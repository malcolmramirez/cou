from typing import List, Callable

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

    def _factor(self) -> AST:
        """
        Parses a factor
            factor : number | bool | string | (disjunction) | (add|sub) factor | variable
        """

        operand_token = self.curr
        node = None

        if operand_token.type == tok.NUMBER:
            self._consume(tok.NUMBER)
            node = Number(operand_token)

        elif operand_token.type == tok.STRING:
            self._consume(tok.STRING)
            node = String(operand_token)

        elif operand_token.type == tok.BOOLEAN:
            self._consume(tok.BOOLEAN)
            node = Boolean(operand_token)

        elif operand_token.type == tok.ID:
            self._consume(tok.ID)
            node = Variable(operand_token)

        elif operand_token.type in (tok.ADD, tok.SUB, tok.NOT):
            self._consume(operand_token.type)
            node = UnaryOperator(operand_token, self._factor())

        elif operand_token.type == tok.L_PAREN:
            self._consume(tok.L_PAREN)
            node = self._disjunction()
            self._consume(tok.R_PAREN)

        return node

    def _parse_binop(self, func: Callable[[], AST], operator_types: List[str]) -> AST:
        """
        Utility method used to parse binary operators
        """

        node = func()
        operator = self.curr

        while operator.type in operator_types:
            self._consume(operator.type)
            node = BinaryOperator(node, operator, func())
            operator = self.curr

        return node

    def _term(self) -> AST:
        """
        Parses a term
            term : factor ((mul|div) factor)*
        """

        return self._parse_binop(self._factor, (tok.MUL, tok.DIV, tok.I_DIV))

    def _sum(self) -> AST:
        """
        Parses a sum
            term : term ((add|sub) term)*
        """

        return self._parse_binop(self._term, (tok.ADD, tok.SUB))

    def _comparison(self) -> AST:
        """
        Parses a boolean comparison
            comparison : sum ((eq|neq|geq|leq|greater|less) sum)*
        """

        return self._parse_binop(self._sum, (tok.EQ, tok.NEQ, tok.GEQ, tok.LEQ, tok.GREATER, tok.LESS))

    def _conjunction(self) -> AST:
        """
        Parses a conjunction
            conjunction : comparison (or comparison)*
        """

        return self._parse_binop(self._comparison, tok.AND)

    def _disjunction(self) -> AST:
        """
        Parses a disjunction
            conjunction : conjunction (and conjunction)*
        """

        return self._parse_binop(self._conjunction, tok.OR)

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

        if token.type not in (tok.INT, tok.REAL, tok.BOOL, tok.STR):
            raise SyntaxError(f"Invalid type definition: {token.value}")

        self._consume(token.type)

        return VariableType(token)

    def _say(self) -> AST:
        """
        Parses a say function
            say : say expression
        """

        self._consume(tok.SAY)
        node = self._disjunction()

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
        assigned = self._disjunction()

        return AssignmentStatement(to_assign, token, assigned)

    def _statement(self) -> AST:
        """
        Parses a statement
            statement : [ empty | assignment_statement | say | expression ] sep
        """

        token = self.curr
        next_char = self._tokenizer.peek()

        if token.type == tok.ID and next_char in (tok.COLON, tok.ASSIGN):
            # Either declaring a variable or assigning.
            stmt = self._assignment_statement()

        elif token.type == tok.SAY:
            stmt = self._say()

        elif token.type == tok.SEP:
            stmt = self._empty()

        else:
            stmt = self._disjunction()

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
