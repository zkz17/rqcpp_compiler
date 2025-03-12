from rqclexer import RQCLexer
from rqcparser import RQCParser
from rqcanalyzer import RQCAnalyzer
from rqctransformer import RQCTransformer
from rqcgenerator import RQCGenerator
import sys

DEBUG = True

def compile(text, debug=False):
    ## Tokenize. 
    text.expandtabs(4)
    lexer = RQCLexer(text)
    lexer.tokenize()
    tokens = lexer.tokens()

    if debug:
        print(' ****** ****** Token List ****** ******')
        print(tokens)
        print()

    ## Generate AST. 
    parser = RQCParser(tokens)
    ast = parser.parse()
    if debug: 
        print(' ****** ****** AST Structure ****** ******')
        ast.print()
        print()

    ## Semantic Analysis.
    analyzer = RQCAnalyzer()
    analyzer.analyze(ast)
    if debug:
        print(' ****** ****** Symbol Table ****** ******')
        ast._symbols.print()
        print()

    ## High-Level Transformation. 
    transformer = RQCTransformer()
    transformer.transform(ast)
    if debug: 
        print(' ****** ****** AST Structure After High-Level Transformation ****** ******')
        ast.print()
        print()

    ## Code Generation.
    generator = RQCGenerator()
    code, mid, mem = generator.generate(ast)
    if debug:
        print(' ****** ****** Mid-Level Code ****** ******')
        mid.print()
        print()
        print(' ****** ****** Memory Allocation ****** ******')
        mem.print()
        print()
        print(' ****** ****** Low-Level Code ****** ******')
        code.print()

    return code

def main():
    ## Locate input & output files. 
    input_path='./test/test.rqcpp'
    if len(sys.argv) <= 1: 
        print('RQC++ Version 0.1.0')
        exit(0)
    elif len(sys.argv) >= 2: 
        input_path = sys.argv[1]
        if not input_path.endswith('.rqcpp'):
            print('Unexpected input file format! Expected: .rqcpp, Received: ', input_path)
            exit(0)
    
    path = input_path[:-6]
    output_path = path + '.qins'

    ## Read input file. 
    text = ''
    try: 
        f = open(input_path, mode='r')
        text = f.read()
        f.close()
    except:
        print('Failed to open file ', input_path)
        exit(0)

    code = compile(text, DEBUG)
    code.write(output_path)

if __name__ == "__main__": 
    main()