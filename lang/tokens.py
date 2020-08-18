# Non Terminals
INT_CONST = "iconst"
REAL_CONST = "rconst"

ID = "id"
EOF = "eof"

TYPE = "type"

# Terminals
ADD = "add"
SUB = "sub"
ROUND = "round"

MUL = "mul"
DIV = "div"
I_DIV = "idiv"

L_PAREN = "lparen"
R_PAREN = "rparen"

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

# Currently unadded types ->
T_STR = "str"
T_BOOL = "bool"

switch = {
    "+"  : ADD,
    "-"  : SUB,
    "*"  : MUL,
    "/"  : DIV,
    "~/" : I_DIV,
    "~"  : ROUND,
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
    SAY
}
