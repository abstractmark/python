import os
import sys
import src.tokenizer
import src.lexer
import src.parser

if len(sys.argv) >= 2:
    f = open(sys.argv[1], 'r')
    tokenizedData = src.tokenizer(f.read())
    lexedData = src.lexer(tokenizedData)
    parsedData = src.parser(lexedData)
    print(parsedData)