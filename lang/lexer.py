import tokens as tkns

# Lexer

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


    def increment(self) -> None:
        """
        Increments pointer in token, updating current char.
        """

        self.index += 1

        if self.index > len(self.input) - 1:
            self.curr = None

        else:
            self.curr = self.input[self.index]


    def trim(self) -> None:
        """
        Trims whitespace past the current index.
        """

        while self.curr and self.curr.isspace():
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
            return Token(tkns.INT, int(number))

        number += self.curr
        self.increment()

        while self.curr and self.curr.isdigit():
            number += self.curr
            self.increment()

        return Token(tkns.REAL, float(number))



    def identifier_token(self) -> Token:
        """
        Parses a variable identifier
        """

        def valid(char: str) -> bool:
            """
            Validates a character to be used in identifier
            """

            return self.curr and \
                (self.curr.isalpha() or self.curr == "_")


        id = ''

        while valid(self.curr):
            id += self.curr
            self.increment()

        return Token(tkns.ID, id)


    def token(self) -> Token:
        """
        Returns next token in stream
        """

        self.trim()

        char = self.curr

        if not char:
            return Token(tkns.EOF, None)

        if char == '.' or char.isdigit():
            return self.number_token()

        if char == "~" and self.next() == "/":
            # Case of integer division
            char += "/"
            self.increment()

        type = tkns.switch.get(char)

        if not type:
            if char.isalpha() or char == "_":
                return self.identifier_token()

            raise TypeError("Invalid syntax \"" + char + "\"")

        token = Token(type, char)
        self.increment()

        return token
