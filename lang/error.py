"""
Utility module used for raising error messages
"""

def error(msg: str, pos = None):
    """
    Utility method to raise SyntaxError
    """

    line = 0
    col = 0

    if type(pos) == tuple:
        line = pos[0]
        col = pos[1]

    elif pos:
        line = pos.line
        col = pos.col

    raise SyntaxError(f"{msg}, <line:{line},col:{col}>")
