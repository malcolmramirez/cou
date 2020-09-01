from typing import Any
from enum import Enum

class FrameTypes(Enum):

    PROGRAM = "program",
    PROCESS = "process",
    CONDITIONAL = "conditional"


class StackFrame(object):
    """
    Represents a frame on the call stack
    """

    def __init__(self, name: str, frame_type: str, sc_level: int, memory = None):

        self.name = name
        self.frame_type = frame_type
        self.sc_level = sc_level

        self.memory = memory if memory else {}

        self.ret_val = None
        self.returned = False

    def __setitem__(self, var_name: str, value: Any) -> None:
        self.memory[var_name] = value

    def __getitem__(self, var_name: str):
        return self.memory[var_name]

    def __str__(self) -> str:
        s = f"{self.sc_level}:{self.name}:{self.frame_type}"
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
