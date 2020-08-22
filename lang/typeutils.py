import codecs
import re

import lang.tokens as tkns

from typing import Any

def decode_escapes(s: str) -> str:
    """
    Decodes escape characters for string tokens
    """

    return codecs.escape_decode(bytes(s, "utf-8"))[0].decode("utf-8")

def is_assignable(cou_type: str, expr: Any) -> bool:
    """
    Checks that the given cou type is appropriate for the expression
    """

    if cou_type == tkns.T_INT:
        return isinstance(expr, int)

    if cou_type == tkns.T_REAL:
        return isinstance(expr, float)

    if cou_type == tkns.T_BOOL:
        return isinstance(expr, bool)

    if cou_type == tkns.T_STR:
        return isinstance(expr, str)

    return False
