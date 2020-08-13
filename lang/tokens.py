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
SEMI = "semi"

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
    ";"  : SEMI,
    "=>" : RETURN
}

# Non Terminals
INT = "int"
REAL = "real"

ID = "id"

EOF = "eof"
