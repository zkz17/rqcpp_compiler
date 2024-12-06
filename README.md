# RQC++ Compiler
(Still under construction)
This is a compiler that supposedly compile the RQC++ language into the low-level QINS instruction set (and probably more). 

## Supported Features
* python-like RQC++ syntax
* if-statement & qif-statement & local-statement & while-statement
* classical array

## Progress
* Tokenization
* AST generation
* AST print
* Scope analysis
* Unitary check
* Symbol table visualization
* Quantum branch rewrite
* Expression extraction rewrite
* Expression split rewrite

## TODO
* PROGRESS: Semantic analysis
  * Type check
  * ...
* PROGRESS: High-level transformation
  * Extract substripted expressions
  * ...
* PROGRESS: QINS code generation
* PROGRESS: Partial evaluation
* FEATURE : Procedure array
* FEATURE : Simultaneous assignment
* DEBUG   : Test cases
* Optional: Optimization passes
* ...