# cou

Cou is a simple programming language

## Instructions

In project directory, run
```
./cou <program-file-name>
```

## Grammar

Cou currently has the following language constructs

(a bit outdated)
### number
#### [0-9]+ | [0-9]* [\.] [0-9]+

Represents an integer or real number

### bool
#### true | false

Represents a boolean

### str
#### ' [.]* '

Represents a string (delimited by ')

### id
#### [[a-z]|[A-Z]| _ ]+

Represents an identifier used for variables/function declarations

### begin
#### \{

Represents the beginning of a function

### end
#### \}

Represents the end of a function

### separator
#### ;

Represents a seprator of lines of code

### type
#### int | real | bool | str

Represents a valid type in cou (either an int or real)

### variable
#### id

Represents a variable with an identifier

### variable_declaration
#### variable [:] type

Represents a variable declaration

### operand
#### number | (expression) | [+|-] operand | variable

Represents an object that can be operated on. (~ is a unary operator for the floor function)

### term
#### operand [\*|/|%/] operand)*

Represents a term, ie, a grouping of multiplication operations done on operands (~/ is integer division)

### expression
#### term [[+|-] term]*

Represents an expression, ie, a grouping of addition operations done on terms

### empty
####

Represents an empty statement

### assignment statement
#### [variable | variable_declaration] [=] expression

Represents an assignment statement, where a variable is assigned the result of san expression

### statement
#### assignment_statement separator | empty separator | expression

Represents a general statement of code

### program
#### statement* eof

Represents a program, ie, a block of statements with the end of file terminating it

## Built in functions

### say
#### Usage : say arg;

Prints the string representation of an argument (parentheses optional)
