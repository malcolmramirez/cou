# cou

Cou is a simple programming language

## Grammar

Cou currently has the following language constructs:

### integer
##### [0-9]+

Represents an integer

### real
##### [0-9]* [\.] [0-9]+

Represents a real number

### number
##### integer | real

Represents an integer or real number

### id
##### ( [a-z] | [A-Z] | _ )+

Represents an identifier used for variables/function declarations

### begin
##### \{

Represents the beginning of a grouping of code

### end
##### \}

Represents the end of a grouping of code

### separator
##### ;

Represents a seprator of lines of code

### variable
##### id

Represents a variable with an identifier

### operand
##### int | real | (expression) | ( + | - | ~ ) operand

Represents an object that can be operated on. (~ is a unary operator for the floor function)

### term
##### operand (\* | / | ~/ ) operand)*

Represents a term, ie, a grouping of multiplication operations done on operands (~/ is integer division)

### expression
##### term (( + | - ) term)*

Represents an expression, ie, a grouping of addition operations done on terms

### empty
#####

Represents an empty statement

### assignment statement
##### variable [=] expression

Represents an assignment statement, where a variable is assigned the result of san expression

### statement
##### compound statement | assignment statement | empty

Represents a general statement of code

### statements
##### statement | statement separator statements

Represents one or more statements

### compound statement
##### begin statements end

Represents many statements surrounded by begin and end blocks, ie, a block of code

### program
##### compound statement eof

Represents a program, ie, a block of code with the end of file terminating it
