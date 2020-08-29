
STRING = "string"
NUMBER = "number"
BOOLEAN = "boolean"

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

SAY = "say"

IF = "if"
ELIF = "elif"
ELSE = "else"

EOF = "eof"


def is_one_char_token(s: str) -> bool:
    """
    Returns true if s is a single character token
    """

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
    """
    Returns true if s is a double character token
    """

    double_char = {
        I_DIV,
        AND, OR,
        EQ, NEQ, GEQ, LEQ
    }

    return s in double_char


def is_keyword(id: str) -> str:
    """
    Returns true if id is a designated keyword
    """

    keywords = {
        NUM, BOOL, STR,
        IF, ELIF, ELSE,
        SAY
    }

    return id in keywords


def is_boolean(id: str) -> bool:
    """
    Returns true if id is a boolean
    """

    return id == 'true' or id == 'false'
