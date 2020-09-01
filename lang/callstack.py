from typing import Any
from enum import Enum

class StackFrame(object):
    """
    Represents a frame on the call stack
    """

    def __init__(self, name: str, sc_level: int, parent = None, memory = None):

        self.name = name
        self.sc_level = sc_level

        self.parent = parent
        self.memory = memory if memory else {}

        self.ret_val = None
        self.returned = False

    def __setitem__(self, var_name: str, value: Any) -> None:
        self.memory[var_name] = value

    def __getitem__(self, var_name: str):
        if var_name in self.memory:
            return self.memory[var_name]

        return self.parent[var_name]

    def __str__(self) -> str:
        s = f"{self.sc_level}:{self.name}:{self.frame_type.value}"
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

    def push(self, frame: StackFrame) -> None:
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
