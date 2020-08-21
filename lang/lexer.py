import lang.tokens as tkns
import lang.typeutils as typeutils

class Token:
    """
    Represents a single token, with a type and value
    """

    def __init__(self, type: str, value: str):
        """
        Initializes token with type and value
        """

        self.type = type
        self.value = value

    def __str__(self) -> str:
        """
        Returns string representation of Token
        """

        return "Token({}, {})".format(self.type, self.value)

    def __repr__(self) -> str:
        """
        Returns string representation of Token
        """

        return self.__str__()


class Lexer:
    """
    Separates input into a stream of tokens.
    """

    def __init__(self, input: str):
        """
        Initializes lexer with a line input. Sets offset from that line and
        initial current character.
        """

        self.input = input
        self.index = 0
        self.curr = None if not input else input[0]

    def next(self) -> str:
        """
        Returns next character in stream without incrementing
        """

        i = self.index + 1

        if i > len(self.input) - 1:
            return None

        return self.input[i]

    def feed(self, input: str) -> None:
        """
        Feeds a new line of input into the lexer
        """

        self.input = input
        self.index = 0
        self.curr = None if not input else input[0]

    def increment(self) -> None:
        """
        Increments pointer in token, updating current char.
        """

        self.index += 1

        if self.index > len(self.input) - 1:
            self.curr = None

        else:
            self.curr = self.input[self.index]

    def skip(self) -> None:
        """
        Skips whitespace and comments
        """

        while self.curr and \
                (self.curr == "#" or self.curr.isspace()):

            while self.curr and self.curr.isspace():
                self.increment()

            if self.curr == "#":
                # Single line comments
                while self.curr and self.curr != "\n":
                    self.increment()

    def number_token(self) -> Token:
        """
        Parses a multi character integer / float, returning a token
        """

        number = ''

        while self.curr and self.curr.isdigit():
            number += self.curr
            self.increment()

        if self.curr != ".":
            return Token(tkns.INT_CONST, int(number))

        number += self.curr
        self.increment()

        while self.curr and self.curr.isdigit():
            number += self.curr
            self.increment()

        return Token(tkns.REAL_CONST, float(number))

    def id_token(self) -> Token:
        """
        Parses a variable identifier, type, or keyword
        """

        def valid(char: str) -> bool:
            """
            Validates a character to be used in identifier
            """

            return self.curr and \
                (self.curr.isalnum() or self.curr == "_")

        id = ''

        while valid(self.curr):
            id += self.curr
            self.increment()

        if id in tkns.types:
            return Token(tkns.TYPE, id)

        elif id in tkns.keywords:
            return Token(id, id)

        return Token(tkns.ID, id)

    def string_token(self) -> Token:
        """
        Parses a string
        """

        s = ''

        prev = self.curr
        self.increment()

        while self.curr != "'" or (prev == "\\" and self.curr == "'"):
            s += self.curr
            prev = self.curr
            self.increment()

        self.increment()

        # Decode escape characters
        return Token(tkns.STR_CONST, typeutils.decode_escapes(s))


    def token(self) -> Token:
        """
        Returns next token in stream
        """

        self.skip()

        char = self.curr

        if not char:
            return Token(tkns.EOF, None)

        elif char == "'":
            return self.string_token()

        elif char == '.' or char.isdigit():
            return self.number_token()

        elif char == "%" and self.next() == "/":
            # Case of integer division
            char += "/"
            self.increment()

        type = tkns.switch.get(char)

        if not type:
            # If we haven't got a type returned, this is an identifier
            if char.isalpha() or char == "_":
                return self.id_token()

            raise SyntaxError("Invalid identifier character: {}".format(char))

        token = Token(type, char)
        self.increment()

        return token
