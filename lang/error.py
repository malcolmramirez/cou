"""
Utility module used for raising error messages
"""

def error(msg: str, token = None, pos = None):
    """
    Utility method to raise SyntaxError
    """

    line = 0
    col = 0

    if token:
        line = token.line
        col = token.col

    elif pos:
        line = pos[0]
        col = pos[1]


    raise SyntaxError(f"{msg}, <line:{line},col:{col}>")
