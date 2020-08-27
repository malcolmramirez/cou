from typing import Any
import lang.token as tok

def valid_type(cou_type: str, asn: Any):
    """
    Validates a cou type given an assignment
    """

    type_switch = {
        tok.INT  : int,
        tok.REAL : float,
        tok.BOOL : bool,
        tok.STR  : str
    }

    c_type = type_switch[cou_type]
    
    return (c_type == type(asn)) or (c_type == float and type(asn) == int)

def valid_operation(op1: Any, op2: Any, op_type: str):
    """
    Validates a cou type given an assignment
    """

    rev_type_switch = {
        int   : tok.NUMBER,
        float : tok.NUMBER,
        bool  : tok.BOOL,
        str   : tok.STR
    }

    c_type_1 = rev_type_switch[type(op1)]
    c_type_2 = rev_type_switch[type(op2)]

    if c_type_1 != c_type_2:
        return False

    op_switch = {
        tok.NUMBER : (tok.ADD, tok.SUB, tok.MUL, tok.DIV, tok.I_DIV),
        tok.BOOL : (tok.AND, tok.OR, tok.NOT),
        tok.STR : (tok.ADD)
    }

    return op_type in op_switch[c_type_1]
