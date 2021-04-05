import os
import sys
import src.tokenizer
import src.lexer
import src.parser

args = sys.argv
if len(args) >= 2:
    f = open(sys.argv[1], 'r')
    tokenizedData = src.tokenizer(f.read())
    lexedData = src.lexer(tokenizedData)
    parsedData = src.parser(lexedData)
    # Check CLI args
    styled = True
    fullHTMLTags = True
    htmlFileName = None
    for arg in args:
        if(arg == "-t" or arg == "--tags"): fullHTMLTags = False
        elif(arg == "-unstyled" or arg == "--unstyled"): styled = False
        if(not arg.startswith('-')): htmlFileName = f"{'.'.join(arg.split('.')[:-1])}.html"
    
    with open(htmlFileName, 'w') as f:
        f.write(parsedData["html"])
else:
    print("\nUsage: abstractmark [abstractmark file] [abstractmark options] [args]\n\nSee \"abstractmark --help\" for more.\n")