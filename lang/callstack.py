from typing import Any
from enum import Enum

class Record(object):

    def __init__(self, context = None):
        self.memory = {}
        self.context = context

    def __setitem__(self, var_name: str, value: Any) -> None:
        if self.context and var_name in self.context:
            self.context[var_name] = value
        else:
            self.memory[var_name] = value

    def __getitem__(self, var_name: str):
        if var_name in self.memory:
            return self.memory[var_name]

        elif self.context:
            return self.context[var_name]

        return None

    def __contains__(self, var_name: str) -> bool:
        return self[var_name] != None

class ActivationRecord(Record):
    """
    Represents a frame on the call stack
    """

    def __init__(self, name: str, sc_level: int, curr_frame = None):

        super().__init__()

        self.name = name
        self.sc_level = sc_level

        self.context = None
        if curr_frame:
            self._find_context(curr_frame)

        self.ret_val = None
        self.returned = False

    def _find_context(self, curr_frame: Record):

        nest_lvl = curr_frame.sc_level - self.sc_level + 1
        self.context = curr_frame

        for i in range(nest_lvl):
            self.context = self.context.context

    def __str__(self) -> str:
        cont = 'TOP_LEVEL'
        if self.context:
            cont = str(self.context)

        s = f"{cont}\n{self.sc_level}:{self.name}"
        for key in self.memory:
            s += f"\n{key} : {self.memory[key]}"

        return s

    __repr__ = __str__


class CallStack(object):
    """
    Represents a call stack
    """

    def __init__(self):
        self.stack = []

    def push(self, frame: Record) -> None:
        """
        Pushes an item onto the stack
        """

        self.stack.append(frame)

    def pop(self) -> Any:
        """
        Pops an item off of the stack
        """

        return self.stack.pop().ret_val

    def peek(self) -> Any:
        """
        Returns the top record from the stack
        """

        return self.stack[-1]

    def __str__(self) -> str:
        s = "call stack"
        for frame in reversed(self.stack):
            s += f"\n{frame}"

        return s

    __repr__ = __str__
