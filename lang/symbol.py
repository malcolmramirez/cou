
import lang.token as tok

from collections import defaultdict
from typing import Any

class Symbol(object):
    """
    Superclass for symbols
    """

    def __init__(self, name: str, type_def = None):
        self.name = name
        self.type_def = type_def

    def __repr__(self) -> str:
        return str(self)


class VariableSymbol(Symbol):
    """
    Represents a variable symbol (with an identifier and type)
    """

    def __init__(self, name: str, type_def: str = None):
        super().__init__(name, type_def)

    def __str__(self) -> str:
        return f"<{self.type_def}:{self.name}>"


class SymbolTable(object):
    """
    Represents a symbol table
    """

    def __init__(self):
        self.symbols = defaultdict()

    def __str__(self) -> str:
        s = "SymbolTable: "
        for key in self.symbols:
            s += f"\n  {self.symbols[key]}"

        return s

    def put(self, symbol: Symbol):
        """
        Puts a symbol in the table
        """

        self.symbols[symbol.name] = symbol

    def get(self, key: str) -> Symbol:
        """
        Retrieves a symbol from the table
        """

        return self.symbols[key]

    def exists(self, key: str):
        """
        Returns true if a symbol exists in the table
        """

        return key in self.symbols

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

    return (c_type == type(asn)) or (c_type == float and isinstance(asn, int))

def valid_operation(op1: Any, op2: Any):
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

    return c_type_1 == c_type_2
