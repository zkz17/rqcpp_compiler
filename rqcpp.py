from rqclexer import RQCLexer
from rqcparser import RQCParser
import sys

DEBUG = True

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

    ## Tokenize. 
    text.expandtabs(4)
    lexer = RQCLexer(text)
    lexer.tokenize()
    tokens = lexer.tokens()

    if DEBUG:
        print(' ****** ****** Program Text ****** ******')
        print(input_path, '--->\n', text)
        print(' ****** ****** Tokens ****** ******')
        print(tokens)

    ## Generate AST. 
    parser = RQCParser(tokens)
    ast = parser.parse()
    if DEBUG: 
        ast.print()

    ## TODO

if __name__ == "__main__": 
    main()