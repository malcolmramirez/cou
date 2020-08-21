# Non Terminals
INT_CONST = "iconst"
REAL_CONST = "rconst"

BOOL_T = "true"
BOOL_F = "false"

STR_CONST = "sconst"

ID = "id"
EOF = "eof"

TYPE = "type"
CHAR = "char"

# Terminals
ADD = "add"
SUB = "sub"

NOT = "not"
AND = "and"
OR = "or"

MUL = "mul"
DIV = "div"
I_DIV = "idiv"

L_PAREN = "lparen"
R_PAREN = "rparen"

QUOTE = "quote"

START = "start"
RETURN = "return"
END = "end"

ASSIGN = "assign"
SEP = "sep"
COLON = "colon"

COMMENT = "comment"

# Keywords
SAY = "say"

# Types
T_INT = "int"
T_REAL = "real"
T_BOOL = "bool"
T_STR = "str"

switch = {
    "+"  : ADD,
    "-"  : SUB,
    "*"  : MUL,
    "/"  : DIV,
    "%/" : I_DIV,
    "~"  : NOT,
    "&:" : AND,
    "?:" : OR,
    "'"  : QUOTE,
    "("  : L_PAREN,
    ")"  : R_PAREN,
    "{"  : START,
    "}"  : END,
    "="  : ASSIGN,
    ";"  : SEP,
    ":"  : COLON,
    "#"  : COMMENT,
    "=>" : RETURN
}

types = {
    T_INT, T_REAL, T_STR, T_BOOL
}

keywords = {
    SAY, BOOL_T, BOOL_F
}
