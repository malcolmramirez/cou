import codecs
import re

def decode_escapes(s: str) -> str:
    """
    Decodes escape characters for string tokens
    """

    return codecs.escape_decode(bytes(s, "utf-8"))[0].decode("utf-8")
