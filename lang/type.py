from typing import Any
import lang.token as tok

_type_switch = {
    int   : tok.NUM,
    float : tok.NUM,
    bool  : tok.BOOL,
    str   : tok.STR
}

def valid_type(cou_type: str, asn: Any):
    """
    Validates a cou type given an assignment
    """

    return cou_type == _type_switch[type(asn)]

def valid_operation(op_type: str, op1: Any, op2: Any = None):
    """
    Validates a cou type given an assignment
    """

    c_type_1 = _type_switch[type(op1)]

    if op2:
        c_type_2 = _type_switch[type(op2)]

        if c_type_1 != c_type_2:
            return False

    op_switch = {
        tok.NUM : (tok.ADD, tok.SUB, tok.MUL, tok.DIV, tok.I_DIV, tok.EQ,
                      tok.NEQ, tok.GEQ, tok.LEQ, tok.GREATER, tok.LESS),
        tok.BOOL   : (tok.AND, tok.OR, tok.NOT, tok.EQ, tok.NEQ),
        tok.STR    : (tok.ADD, tok.EQ, tok.NEQ)
    }

    return op_type in op_switch[c_type_1]
