# RQC++ Compiler
(Still under construction)
This is a compiler that supposedly compile the RQC++ language into the low-level QINS instruction set (and probably more). 

## Supported Features
* python-like RQC++ syntax
* if-statement & qif-statement & local-statement & while-statement

## Progress
* Tokenization
* AST generation
* AST print
* Scope analysis
* Quantum branch rewrite
* Expression extraction rewrite
* Expression split rewrite

## TODO
* PROGRESS: Semantic analysis
  * Unitary gate
  * ...
* PROGRESS: QINS code generation
* PROGRESS: Partial evaluation
* FEATURE : Classical variable array
* FEATURE : Procedure array
* DEBUG   : Symbol table visualization
* DEBUG   : Test cases
* Optional: Optimization passes
* ...