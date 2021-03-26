import os
import sys
import src.tokenizer
import src.lexer

if len(sys.argv) >= 2:
    f = open(sys.argv[1], 'r')
    tokenized = src.tokenizer(f.read())
    print(src.lexer(tokenized))