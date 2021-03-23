import os
import sys
import src.tokenizer

if len(sys.argv) >= 2:
    f = open(sys.argv[1], 'r')
    print(src.tokenizer(f.read()))