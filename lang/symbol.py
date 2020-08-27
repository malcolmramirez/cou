
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
