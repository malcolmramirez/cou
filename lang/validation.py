from typing import Any

from lang.tokenizer import Token
import lang.token as tok

_type_switch = {
    int   : tok.NUM,
    float : tok.NUM,
    bool  : tok.BOOL,
    str   : tok.STR
}

_op_switch = {
    tok.NUM    : (tok.ADD, tok.SUB, tok.MUL, tok.DIV, tok.I_DIV, tok.EQ,
                  tok.NEQ, tok.GEQ, tok.LEQ, tok.GREATER, tok.LESS),
    tok.BOOL   : (tok.AND, tok.OR, tok.NOT, tok.EQ, tok.NEQ),
    tok.STR    : (tok.ADD, tok.EQ, tok.NEQ)
}


def validate_type(cou_type: str, pos: list, asn: Any):
    """
    Validates a cou type given an assignment
    """

    asn_c_type = _type_switch[type(asn)]
    if cou_type != asn_c_type:
        raise SyntaxError(f"Cannot assign type \'{asn_c_type}\' to \'{cou_type}\' <line:{pos[0]},col:{pos[1]}>")

def validate_operation(op_type: str, pos: list, op1: Any, op2: Any = None):
    """
    Validates a cou type given an operation
    """

    c_type_1 = _type_switch[type(op1)]

    if op2:
        c_type_2 = _type_switch[type(op2)]
        if c_type_1 != c_type_2:
            raise SyntaxError(f"Invalid operation {op_type} between types '{c_type_1}' and '{c_type_2}' <line:{pos[0]},col:{pos[1]}>")

    else:
        if op_type not in _op_switch[c_type_1]:
            raise SyntaxError(f"Invalid operation {op_type} for type '{c_type_1}' <line:{pos[0]},col:{pos[1]}>")
