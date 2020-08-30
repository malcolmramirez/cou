import codecs
import lang.token as tok

class Token:
    """
    Represents a single token, with a type and value
    """

    def __init__(self, type: str, value: str, line: int, col: int):
        """
        Initializes token with type and value
        """

        self.type = type
        self.value = value
        self.line = line
        self.col = col

    def __str__(self) -> str:
        """
        Returns string representation of Token
        """

        return f"Token<{self.type},{self.value},{self.line},{self.col}>"

    def __repr__(self) -> str:
        """
        Returns string representation of Token
        """

        return self.__str__()

class Tokenizer(object):

    def __init__(self, input: str):
        """
        Initializes tokenizer with an input. Sets offset from that line and
        initial current character.
        """

        self.input = input
        self.index = 0

        self.curr = input[0] if input else None

        self.line = 1
        self.col = 1

        self.keywords = tok.build_keywords()

    def _next(self) -> str:
        """
        Returns next character in stream without incrementing
        """

        i = self.index + 1

        if i >= len(self.input):
            return None

        return self.input[i]

    def _increment(self) -> str:
        """
        Increments pointer in token, updating current char.
        Returns curr for convenience
        """

        prev = self.curr

        self.curr = self._next()
        self.index += 1
        self.col += 1

        return prev

    def _skip(self) -> None:
        """
        Skips whitespace and comments
        """

        while self.curr and (self.curr == '#' or self.curr.isspace()):

            while self.curr and self.curr.isspace():
                if self.curr == '\n':
                    self.line += 1
                    self.col = 0

                self._increment()

            if self.curr != "#":
                return

            while self.curr and self.curr != "\n":
                self._increment()  # Single line comments

    def _number_token(self) -> Token:
        """
        Parses a multi character integer / float, returning a token
        """

        t_type = tok.NUMBER
        num = ''

        while self.curr and self.curr.isdigit():
            num += self._increment()

        if self.curr != ".":
            return Token(t_type, int(num), self.line, self.col)

        num += self._increment()

        while self.curr and self.curr.isdigit():
            num += self._increment()

        return Token(t_type, float(num), self.line, self.col)

    def _name_token(self) -> Token:
        """
        Parses a name, ie, something that is signified by a sequence of characters
        (that is not a string)
        name : id or boolean or keyword
        """

        t_type = tok.ID
        id = ''

        while self.curr and (self.curr.isalnum() or self.curr == "_"):
            id += self._increment()

        if id in self.keywords:
            return Token(id, id, self.line, self.col)

        return Token(tok.ID, id, self.line, self.col)

    def _string_token(self) -> Token:
        """
        Parses a string
        """

        t_type = tok.STRING
        string = ''

        prev = self._increment()

        while self.curr != "'" or (prev == "\\" and self.curr == "'"):
            string += self.curr
            prev = self._increment()

        self._increment()

        # Decode escape characters
        decoded_string = codecs.escape_decode(
            bytes(string, "utf-8"))[0].decode("utf-8")

        return Token(t_type, decoded_string, self.line, self.col)

    def peek(self) -> str:
        """
        Destructively searches through the stream to return the next non
        whitespace or non comment char. Use carefully
        """

        next_char = self._next()

        if not next_char or not next_char.isspace():
            return next_char

        self._skip()

        return self.curr

    def produce(self) -> Token:
        """
        Returns next token in stream
        """

        self._skip()

        char = self.curr

        if not char:
            return Token(tok.EOF, None, self.line, self.col)

        elif char == '\'':
            return self._string_token()

        elif char == '.' or char.isdigit():
            return self._number_token()

        elif char.isalpha() or char == '_':
            return self._name_token()

        poss_tok = char + self._next()

        if poss_tok in tok.reserved_double_char:
            char = poss_tok
            self._increment()

        elif char not in tok.reserved_single_char:
            # If there is not a one char identifier at this point, bad char.
            raise SyntaxError(f"Invalid character: {char} <line:{self.line},col:{self.col}>")

        token = Token(char, char, self.line, self.col)
        self._increment()

        return token
