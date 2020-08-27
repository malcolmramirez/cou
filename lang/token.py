
STRING = "string"
NUMBER = "number"
BOOLEAN = "boolean"

ID = "id"
INT = "int"
REAL = "real"
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

SAY = "say"
TOI = "toi"
TOR = "tor"
TOB = "tob"
TOS = "tos"

EOF = "eof"


def is_one_char_token(s: str) -> bool:
    single_char = {
        ADD, SUB, MUL, DIV,
        NOT,
        GREATER, LESS,
        L_PAREN, R_PAREN,
        L_BRACE, R_BRACE,
        ASSIGN, COLON,
        SEP
    }

    return s in single_char


def is_two_char_token(s: str) -> bool:
    double_char = {
        I_DIV,
        AND, OR,
        EQ, NEQ, GEQ, LEQ
    }

    return s in double_char


def is_keyword(id: str) -> str:
    keywords = {
        INT, REAL, BOOL, STR, SAY
    }

    return id in keywords


def is_boolean(id: str) -> bool:
    return id == 'true' or id == 'false'
