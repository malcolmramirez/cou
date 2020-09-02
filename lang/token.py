
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
ARR = "arr"

ADD = "+"
SUB = "-"
MUL = "*"
DIV = "/"
MOD = "%"
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

L_BRACK = "["
R_BRACK = "]"

ASSIGN = "="

SEP = ";"
COLON = ":"
COMMA = ","

SAY = "say"
PROC = "proc"
RETURN = "return"
AS = "as"

IF = "if"
ELIF = "elif"
ELSE = "else"

EOF = "eof"

reserved_single_char = {
    ADD, SUB, MUL, DIV, MOD,
    NOT,
    GREATER, LESS,
    L_PAREN, R_PAREN,
    L_BRACE, R_BRACE,
    L_BRACK, R_BRACK,
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
        NUM, STR, BOOL, ARR, NIL,
        PROC, RETURN, AS,
        BOOL_T, BOOL_F, NOTHING,
        IF, ELIF, ELSE,
        SAY
    }
