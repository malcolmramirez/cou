
from lang.tokenizer import Token

STRING = "string"
NUMBER = "number"
BOOLEAN = "boolean"
NIL = "nil"

BOOL_T = "true"
BOOL_F = "false"

NOTHING = "nothing"

ID = "id"
NUM = "num"
BOOL = "bool"
STR = "str"

ADD = "+"
SUB = "-"
MUL = "*"
DIV = "/"
I_DIV = "%/"

NOT = "!"
AND = "&&"
OR = "||"
EQ = "=="
NEQ = "!="
GREATER = ">"
LESS = "<"
GEQ = ">="
LEQ = "<="

L_PAREN = "("
R_PAREN = ")"

L_BRACE = "{"
R_BRACE = "}"

ASSIGN = "="

SEP = ";"
COLON = ":"
COMMA = ","

SAY = "say"
PROC = "proc"
RETURN = "return"

IF = "if"
ELIF = "elif"
ELSE = "else"

EOF = "eof"

reserved_single_char = {
    ADD, SUB, MUL, DIV,
    NOT,
    GREATER, LESS,
    L_PAREN, R_PAREN,
    L_BRACE, R_BRACE,
    ASSIGN, COLON, COMMA,
    SEP
}

reserved_double_char = {
    I_DIV,
    AND, OR,
    EQ, NEQ, GEQ, LEQ
}


def build_keywords() -> dict:
    return {
        NUM, STR, BOOL, NIL,
        PROC, RETURN,
        BOOL_T, BOOL_F, NOTHING,
        IF, ELIF, ELSE,
        SAY
    }
