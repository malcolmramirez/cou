
STRING = "string"
NUMBER = "number"
BOOLEAN = "boolean"

ID = "id"
INT = "int"
REAL = "real"
BOOL = "bool"
STR = "str"

ADD = "add"
SUB = "sub"
MUL = "mul"
DIV = "div"
I_DIV = "idiv"

NOT = "not"

L_PAREN = "lparen"
R_PAREN = "rparen"

L_BRACE = "lbrace"
R_BRACE = "rbrace"

ASSIGN = "assign"

SEP = "sep"
COLON = "colon"

SAY = "say"
EOF = "eof"


def one_char_token(s: str) -> str:
    single_char_switch = {
        '+': ADD,
        '-': SUB,
        '*': MUL,
        '/': DIV,
        '(': L_PAREN,
        ')': R_PAREN,
        '{': L_BRACE,
        '}': R_BRACE,
        '=': ASSIGN,
        ':': COLON,
        ';': SEP
    }

    if s not in single_char_switch:
        return None

    return single_char_switch[s]


def two_char_token(s: str) -> str:
    double_char_switch = {
        '%/': I_DIV
    }

    if s not in double_char_switch:
        return None

    return double_char_switch[s]


def is_keyword(id: str) -> str:
    keywords = {
        INT, REAL, BOOL, STR, SAY
    }

    return id in keywords


def is_boolean(id: str) -> bool:
    return id == 'true' or id == 'false'
