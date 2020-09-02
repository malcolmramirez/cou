from typing import Any

from lang.tokenizer import Token
from lang.error import error

import lang.token as tok

_type_switch = {
    int        : tok.NUM,
    float      : tok.NUM,
    bool       : tok.BOOL,
    str        : tok.STR,
    list       : tok.ARR,
    type(None) : tok.NIL
}

_op_switch = {
    tok.NUM    : (tok.ADD, tok.SUB, tok.MUL, tok.DIV, tok.MOD, tok.I_DIV,
                  tok.EQ, tok.NEQ, tok.GEQ, tok.LEQ, tok.GREATER, tok.LESS),
    tok.BOOL   : (tok.AND, tok.OR, tok.NOT, tok.EQ, tok.NEQ),
    tok.STR    : (tok.ADD, tok.EQ, tok.NEQ),
    tok.NIL    : (tok.EQ, tok.NEQ),
    tok.ARR    : (tok.EQ, tok.NEQ)
}


def validate_array_index(token: Token, index: Any, arr: Any):
    """
    Validates an array index
    """

    arr_c_type = _type_switch[type(arr)]
    if type(index) != int:
        error(f"Array index must be an integer value", token)

    elif type(arr) != list:
        error(f"Type '{arr_c_type}' not indexed", token)

    elif len(arr) <= index:
        raise IndexError(f"Array index out of range <line:{token.line},col:{token.col}>")


def validate_array_size(token: Token, asn: Any):
    """
    Validates an array assignment
    """

    if type(asn) != int:
        error(f"Array size must be an integer value", token)


def validate_condition(token: Token, asn: Any):
    """
    Validates a cou type given given a function return type
    """

    asn_c_type = _type_switch[type(asn)]
    if tok.BOOL != asn_c_type:
        error(f"Condition cannot be \'{asn_c_type}\', must evaluate to 'bool'", token)

def validate_return(cou_type: str, token: Token, asn: Any):
    """
    Validates a cou type given given a function return type
    """

    asn_c_type = _type_switch[type(asn)]
    if cou_type != asn_c_type:
        error(f"Incompatible type \'{asn_c_type}\' for return type \'{cou_type}\'", token)


def validate_type(cou_type: str, token: Token, asn: Any):
    """
    Validates a cou type given an assignment
    """

    asn_c_type = _type_switch[type(asn)]
    if cou_type != asn_c_type:
        error(f"Cannot assign \'{asn_c_type}\' to \'{cou_type}\'", token)

def validate_operation(op_type: str, token: Token, op1: Any, op2: Any = None):
    """
    Validates a cou type given an operation
    """

    c_type_1 = _type_switch[type(op1)]

    if op2:

        c_type_2 = _type_switch[type(op2)]

        if (c_type_1 == tok.STR or c_type_2 == tok.STR) and op_type == tok.ADD:
            return # Here an automatic string conversion will happen, so this is ok

        if c_type_1 != c_type_2 or op_type not in _op_switch[c_type_1]:
            error(f"Invalid operation {op_type} between types '{c_type_1}' and '{c_type_2}'", token)

    else:
        if op_type not in _op_switch[c_type_1]:
            error(f"Invalid operation {op_type} for type '{c_type_1}'", token)
