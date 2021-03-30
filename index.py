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
    # Check CLI args
    args = sys.argv[2::]
    styled = True
    fullHTMLTags = True
    for arg in args:
        if(arg == "-t" or arg == "--tags"): fullHTMLTags = False
        elif(arg == "-unstyled" or arg == "--unstyled"): styled = False