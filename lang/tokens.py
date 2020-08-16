# Non Terminals
INT = "int"
I_CON = "icon"

REAL = "real"
R_CON = "rcon"

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

MAIN = "main"

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
    "=>" : RETURN
}
