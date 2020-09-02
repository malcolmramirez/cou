from typing import List, Callable, Any

import lang.token as tok

from lang.tokenizer import Tokenizer
from lang.error import error

from lang.ast import *
from lang.symtab import *

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

        # Stores types for variables (used for validation)
        self.symtab = SymbolTable(1, "global", None)

    def _consume(self, type: str) -> None:
        """
        Consumes a token of the specified type, raising an error if the current
        token in the stream is not that type.
        """

        if self.curr.type != type:
            error(f"Expected '{type}'", self.curr)

        self.curr = self._tokenizer.produce()

    def _factor(self) -> AST:
        """
        Parses a factor
            factor : number | bool | string | (disjunction) | (add|sub) factor | variable
        """

        operand_token = self.curr
        node = None

        if operand_token.type == tok.ARR:
            node = self._array_initialization()

        elif operand_token.type == tok.ID:
            next_char = self._tokenizer.peek()

            if next_char == tok.L_PAREN:
                node = self._process_call()

            elif next_char == tok.L_BRACK:
                node = self._array_element()

            else:
                node = self._variable()

        elif operand_token.type == tok.NUMBER:
            self._consume(tok.NUMBER)
            node = Number(operand_token)

        elif operand_token.type == tok.STRING:
            self._consume(tok.STRING)
            node = String(operand_token)

        elif operand_token.type == tok.NOTHING:
            self._consume(tok.NOTHING)
            node = Nothing(operand_token)

        elif operand_token.type in (tok.BOOL_T, tok.BOOL_F):
            self._consume(operand_token.type)
            node = Boolean(operand_token)

        elif operand_token.type in (tok.ADD, tok.SUB, tok.NOT):
            self._consume(operand_token.type)
            node = UnaryOperator(operand_token, self._factor())

        elif operand_token.type == tok.L_PAREN:
            self._consume(tok.L_PAREN)
            node = self._disjunction()
            self._consume(tok.R_PAREN)

        else:
            error(f"Invalid factor '{operand_token.value}'", operand_token)

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

        return self._parse_binop(self._factor, (tok.MUL, tok.DIV, tok.MOD, tok.I_DIV))

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

    def _array_element(self) -> AST:
        """
        Parses an array element
            array_element : id lbrack number rbrack
        """

        token = self.curr
        arr_name = token.value

        if arr_name not in self.symtab:
            error(f"Array '{arr_name}' accessed before declaration", token)

        self._consume(tok.ID)

        indices = []
        while self.curr.type == tok.L_BRACK:
            self._consume(tok.L_BRACK)
            indices.append(self._sum())
            self._consume(tok.R_BRACK)

        return ArrayElement(token, indices)

    def _variable(self) -> AST:
        """
        Parses a variable
            variable : id
        """

        token = self.curr
        var_name = token.value

        if var_name not in self.symtab:
            error(f"Variable '{var_name}' referenced before declaration", token)

        var_type = self.symtab[var_name].type_def
        self._consume(tok.ID)

        return Variable(token, var_type)

    def _variable_type(self) -> AST:
        """
        Parses a type
            type : num | bool | str | nil | arr
        """

        token = self.curr

        if token.type not in (tok.NUM, tok.BOOL, tok.STR, tok.NIL, tok.ARR):
            error(f"Invalid type definition: '{token.value}'", token)

        self._consume(token.type)

        return VariableType(token)

    def _variable_declaration(self) -> AST:
        """
        Parses a variable declaration
            variable_declaration : variable colon variable_type
        """

        token = self.curr
        var_name = token.value

        if var_name in self.symtab:
            error(f"Variable '{var_name}' declared more than once", token)

        self._consume(tok.ID)
        self._consume(tok.COLON)

        var_type = self._variable_type()
        variable = Variable(token, var_type.value)

        self.symtab[var_name] = VariableSymbol(var_name, var_type.value)

        return VariableDeclaration(variable, var_type)

    def _array_initialization(self) -> AST:
        """
        Parses an array initialization
            array : arr lbrack sum rbrack
        """

        token = self.curr

        self._consume(tok.ARR)

        self._consume(tok.L_BRACK)
        arr = ArrayInitialization(token, self._sum())
        self._consume(tok.R_BRACK)

        return arr

    def _assignment_statement(self) -> AST:
        """
        Parses an assignment statement
            statement : variable assign disjunction
                            | variable_declaration assign disjunction
                            | variable_declaration assign array
                            | array_element_assignment
        """

        token = self.curr
        var_name = token.value

        next_char = self._tokenizer.peek()

        if next_char == tok.L_BRACK:
            to_assign = self._array_element()
            self._consume(tok.ASSIGN)
            return ArrayElementAssignment(to_assign, token, self._disjunction())

        if next_char == tok.COLON:
            to_assign = self._variable_declaration()

        else:
            to_assign = self._variable()

        self._consume(tok.ASSIGN)

        if self.curr.type == tok.ARR:
            return AssignmentStatement(to_assign, token, self._array_initialization())

        return AssignmentStatement(to_assign, token, self._disjunction())

    def _condition(self) -> AST:
        """
        Parses a conditional block
        """

        token = self.curr
        conditions = []

        scope_level = self.symtab.sc_level + 1

        self._consume(tok.IF)

        self._consume(tok.L_PAREN)
        condition = self._disjunction()
        self._consume(tok.R_PAREN)

        # Shifting the scope of the symbol table to the conditional level
        self.symtab = SymbolTable(scope_level, "if", self.symtab)
        conditions.append(Condition(condition, self._block()))
        self.symtab = self.symtab.sc_enclosing

        while self.curr.type == tok.ELIF:
            self._consume(tok.ELIF)

            self._consume(tok.L_PAREN)
            condition = self._disjunction()
            self._consume(tok.R_PAREN)

            self.symtab = SymbolTable(scope_level, "elif", self.symtab)
            conditions.append(Condition(condition, self._block()))
            self.symtab = self.symtab.sc_enclosing

        if self.curr.type == tok.ELSE:
            # Use this to always eval True for else during interpretation
            else_tok = self.curr
            else_tok.value = tok.BOOL_T
            else_cond = Boolean(else_tok)

            self._consume(tok.ELSE)

            self.symtab = SymbolTable(scope_level, "else", self.symtab)
            conditions.append(Condition(else_cond, self._block()))
            self.symtab = self.symtab.sc_enclosing

        return Conditions(conditions)

    def _as_declaration(self) -> AST:
        """
        Parses the declaration of an 'as' block
            as_declaration : lparen (assignment_statement sep)? disjunction sep (assignment_statement sep)?
        """

        self._consume(tok.L_PAREN)

        token = self.curr
        next_char = self._tokenizer.peek()
        var_declr = None

        if token.type == tok.ID and \
                (next_char == tok.COLON or next_char == tok.ASSIGN):
            # This is an assignment statement
            var_declr = self._assignment_statement()
            self._consume(tok.SEP)

        condition = self._disjunction()

        asn_statement = None
        if self.curr.type != tok.R_PAREN:
            self._consume(tok.SEP)
            asn_statement = self._assignment_statement()

        self._consume(tok.R_PAREN)

        return AsDeclaration(token, var_declr, condition, asn_statement)

    def _as(self) -> AST:
        """
        Parses an 'as' block, ie, a loop
            as: as as_declaration block
        """

        token = self.curr
        self._consume(tok.AS)

        self.symtab = SymbolTable(self.symtab.sc_level + 1, "as", self.symtab)
        as_node = As(token, self._as_declaration(), self._block())
        self.symtab = self.symtab.sc_enclosing

        return as_node

    def _process_declaration(self) -> AST:
        """
        Parses a variable declaration
        """

        token = self.curr
        proc_name = token.value

        if proc_name in self.symtab:
            error(f"Name '{proc_name}' declared more than once", token)

        self._consume(tok.ID)
        self._consume(tok.COLON)

        proc_type = self._variable_type()

        params = []
        self._consume(tok.L_PAREN)

        # Shifting the scope of the symbol table to the processes level
        prev_tab = self.symtab
        self.symtab = SymbolTable(prev_tab.sc_level + 1, proc_name, prev_tab)

        if self.curr.type != tok.R_PAREN:
            params.append(self._variable_declaration())

        while self.curr.type == tok.COMMA:
            self._consume(tok.COMMA)
            params.append(self._variable_declaration())

        prev_tab[proc_name] = ProcessSymbol(proc_name, proc_type.value, self.symtab.sc_level, params)

        self._consume(tok.R_PAREN)

        return ProcessDeclaration(token, proc_type, params)

    def _process(self) -> AST:
        """
        Parses a process
            process : proc id colon type lparen parameters rparen lbrace statements rbrace
        """

        self._consume(tok.PROC)

        proc_dec = self._process_declaration()
        proc_name = proc_dec.value

        block = self._block()
        self.symtab = self.symtab.sc_enclosing

        process = Process(proc_dec, block)

        # Store a pointer to this process node in the process symbol
        self.symtab[proc_name].process = process

        return process

    def _process_call(self) -> AST:
        """
        Parses a call to a process
            process_call : id lparen (disjunction (comma disjunction)*)? rparen
        """

        token = self.curr
        proc_name = token.value

        if proc_name not in self.symtab:
            error(f"Process {proc_name} not defined in current scope", token)

        st_entry = self.symtab[proc_name]

        if not st_entry.is_proc:
            error(f"Identifier {proc_name} does not refer to a process", token)

        self._consume(tok.ID)

        args = []
        self._consume(tok.L_PAREN)

        if self.curr.type != tok.R_PAREN:
            args.append(self._disjunction())

        while self.curr.type == tok.COMMA:
            self._consume(tok.COMMA)
            args.append(self._disjunction())

        self._consume(tok.R_PAREN)

        if len(st_entry.params) != len(args):
            error(f"Incorrect number of args ({len(args)}) for process '{proc_name}'", token)

        return ProcessCall(token, args, st_entry)

    def _return(self) -> AST:
        """
        Parses a return statement
        """

        self._consume(tok.RETURN)

        if (self.curr.value == tok.SEP):
            return Return(Empty())

        return Return(self._disjunction())

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

    def _block(self) -> AST:
        """
        Parses a block of code
        """

        self._consume(tok.L_BRACE)

        statements = []
        while self.curr.type != tok.R_BRACE:
            statements.append(self._statement())

        self._consume(tok.R_BRACE)

        return Block(statements)

    def _statement(self) -> AST:
        """
        Parses a statement
            statement : [ empty | assignment_statement |
                          say | disjunction | conditional
                        ] sep
        """

        token = self.curr
        next_char = self._tokenizer.peek()

        if token.type == tok.PROC:
            return self._process()

        elif token.type == tok.IF:
            return self._condition()

        elif token.type == tok.AS:
            return self._as()

        if token.type == tok.ID and next_char == tok.L_PAREN:
            # Call for a process
            stmt = self._process_call()

        elif token.type == tok.ID and next_char in (tok.COLON, tok.ASSIGN, tok.L_BRACK):
            # Either declaring a variable, assigning, or accessing an array.
            stmt = self._assignment_statement()

        elif token.type == tok.SAY:
            stmt = self._say()

        elif token.type == tok.RETURN:
            stmt = self._return()

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
