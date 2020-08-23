import codecs
import re

import lang.tokens as tkns

from typing import Any

_PYTYPE_MAPPINGS = {
    int   : tkns.T_INT,
    float : tkns.T_REAL,
    bool  : tkns.T_BOOL,
    str   : tkns.T_STR
}

_NUM_TYPES = {
    tkns.T_INT, tkns.T_REAL
}

def __pytype_mapper(obj: Any) -> str:
    """
    Maps a python type to a cou type
    """

    if obj in (tkns.BOOL_T, tkns.BOOL_F):
        # Special case for cou bools -> 'true', 'false' treated as str by python.
        return tkns.T_BOOL

    pytype = type(obj)

    if pytype not in _PYTYPE_MAPPINGS:
        raise SyntaxError("Cou functionality not builtin for pytype {}".format(pytype))

    return _PYTYPE_MAPPINGS[pytype]

def decode_escapes(s: str) -> str:
    """
    Decodes escape characters for string tokens
    """

    return codecs.escape_decode(bytes(s, "utf-8"))[0].decode("utf-8")

def valid_operation(op1: Any, op2: Any) -> bool:

    t1 = __pytype_mapper(op1)
    t2 = __pytype_mapper(op2)

    return (t1 == t2) or (t1 in _NUM_TYPES and t2 in _NUM_TYPES)

def valid_assignment(cou_type: str, expr: Any) -> bool:
    """
    Checks that the given cou type is appropriate for the expression
    """
    
    return __pytype_mapper(expr) == cou_type
