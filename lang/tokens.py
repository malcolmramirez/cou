# Non Terminals
INT = "int"
REAL = "real"

ID = "id"
EOF = "eof"

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

KEYWORD = "keyword"
TYPE = "type"

SAY = "say"

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
    "int"  : INT,
    "real" : REAL
}

keywords = {
    "say" : SAY
}
