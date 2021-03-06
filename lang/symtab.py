import lang.token as tok

from collections import defaultdict
from typing import List, Any


class Symbol(object):
    """
    Superclass for symbols
    """

    def __init__(self, name: str, type_def: str = None):
        self.name = name
        self.type_def = type_def
        self.is_proc = False # Flag for process symbol

    def __repr__(self) -> str:
        return str(self)


class TypeSymbol(Symbol):
    """
    Represents a type symbol (ie, num, bool)
    """

    def __init__(self, name: str):
        super().__init__(name)

    def __str__(self) -> str:
        return f"<{self.name}>"


class VariableSymbol(Symbol):
    """
    Represents a variable symbol (with an identifier and type)
    """

    def __init__(self, name: str, type_def: str):
        super().__init__(name, type_def)

    def __str__(self) -> str:
        return f"var <{self.name}:{self.type_def}>"


class ProcessSymbol(Symbol):
    """
    Represents a symbol for a process
    """

    def __init__(self, name: str, type_def: str, sc_level: int, params: List[VariableSymbol] = None):

        super().__init__(name, type_def)

        self.params = params if params else []
        self.is_proc = True

        self.sc_level = sc_level
        self.process = None

    def __str__(self) -> str:
        param_fmt = ''
        if self.params:
            param_fmt = str(self.params)
            param_fmt = param_fmt[1: len(param_fmt) - 1]

        return f"proc <{self.name}: {self.type_def}({param_fmt})>"


class SymbolTable(object):
    """
    Represents a symbol table
    """

    def __init__(self, sc_level: int, sc_name: str, sc_enclosing=None):
        self._symbols = defaultdict()
        self._init_type_syms()

        self.sc_level = sc_level
        self.sc_name = sc_name
        self.sc_enclosing = sc_enclosing

    def _init_type_syms(self):
        """
        Initalizes type symbols
        """

        self[tok.NUM]  = TypeSymbol(tok.NUM)
        self[tok.BOOL] = TypeSymbol(tok.BOOL)
        self[tok.STR]  = TypeSymbol(tok.STR)
        self[tok.NIL]  = TypeSymbol(tok.NIL)

    def __str__(self) -> str:
        s = f"symtab {self.sc_name}, level:{self.sc_level}"

        for key in self._symbols:
            s += f"\n  {self._symbols[key]}"

        return s

    def __setitem__(self, key: str, symbol: Symbol):
        """
        Puts a symbol in the table
        """

        self._symbols[key] = symbol

    def __getitem__(self, key: str) -> Symbol:
        """
        Retrieves a symbol from the table
        """

        if key not in self._symbols and self.sc_enclosing:
            return self.sc_enclosing[key]

        return self._symbols[key]

    def __contains__(self, key: str):
        """
        Returns true if a symbol exists in the table
        """

        exists_flag = key in self._symbols
        if self.sc_enclosing and not exists_flag:
            exists_flag = key in self.sc_enclosing

        return exists_flag
