# cou

Cou is a simple, statically typed programming language

## Instructions

In project directory, run
```
./cou <program-file-name>
```

## Syntax

### Types

Cou supports the following types

**num** : Represents a number, either an integer or float

**bool** : Represents a boolean, denoted as either 'true' or 'false'

**str** : Represents a string. In cou, strings are delimited by single quotes, ie, ```'hello world'``` is acceptable, but ```"hello world"``` is not.

**nil** : A type to represent nothing, like ```null``` in Java or ```None``` in Python. The keyword used to represent a **nil** type object is ```nothing```

**arr** : Represents an array. In cou, arrays do not have an enforced typing. They are only initialized using a size parameter. For example, ```arr[5]``` will initialize an array with five elements. Each element will assume a ```nothing``` value by default.
Array elements are accessed in typical fashion, ie, for an given an array named a with 3 elements, ```a[2]``` will access the third element in a.

### Variables

Since cou is statically typed, each variable must have a specified type when it is declared. The syntax for a variable declaration is ```identifer: type```.

Cou does not support variable declaration without assignment, so when a variable is declared it must also be assigned a value. For example, ```s: str;``` is not a valid expression, and will cause a parser error.

Below are some valid examples of variable declaration in cou.

```
integer: num = 5; # Creates a number with the value '5'
```

```
b: bool = true; # Creates a 'true' valued boolean
```

```
hello: str = 'hello world'; # Creates a variable 'hello' that stores the string hello world.
```

```
five: arr = arr[5]; # Creates an array with five elements
```

```
nada: nil = nothing; # Creates a 'nil' variable, assigning it 'nothing'
```

### Operations

Cou supports standard comparison ```==, !=, <=, <, >=, >```, logical ```&&, ||, !```, and arithmetic ```+, -, *, /, %``` operations. In cou, there is a distinction between floating point and integer division. The operator ```%/``` has been reserved for integer division. ```/``` is used for floating point division.

Logical operators cannot be applied to arithmetic operators and vice versa. Moreover, all types are comparable to each other (using equality), but not to other types. The operators ```<=, <, >=, >``` are reserved for numeric use only.

The only valid operation for strings aside from comparison is the concatenation operator ```+```. If any other type is concatenated to a string it will automatically be converted to a string value. For example,
```
valid_string: str = 'hello #' + 1 + '!';
```

will result in ```valid_string``` holding the value ```'hello #1!'```.

### Processes

TODO
### Logical Control Flow
TODO
### Repetitive Control Flow
TODO


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
