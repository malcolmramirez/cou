# Non Terminals
INT = "int"
REAL = "real"

ID = "id"
EOF = "eof"

# Terminals
ADD = "add"
SUB = "sub"
FLOOR = "floor"

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

DECL = "decl"
SAY = "say"

switch = {
    "+"  : ADD,
    "-"  : SUB,
    "*"  : MUL,
    "/"  : DIV,
    "~/" : I_DIV,
    "~"  : FLOOR,
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
