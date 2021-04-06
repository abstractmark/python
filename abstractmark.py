import os
import sys
import src.tokenizer
import src.lexer
import src.parser
import webbrowser

HELP_TEXT = """
Usage:
 » For Converting Abstractmark : run "abstractmark [abstractmark file] [abstractmark options] [args]"
 » For Abstractmark's Information : run "abstractmark [option]"
Example:
 » (Convert Markdown to HTML) abstractmark example.am
 » (Convert Markdown to certain HTML file name) abstractmark example.am myfile.html
 » (Checking the Current Version of Abstractmark) abstractmark -v

Abstractmark information options:
 -v, --version ........... show abstractmark current version
 --help .................. informations about AbstractMark CLI

Abstractmark converting options:
 -open ................... Open html file in browser after finish converting. 
 -t, --tags .............. Convert to only HTML file which contains only corresponding tags. (Note that AbstractMark CLI converts to full HTML file as default)
 -unstyled ............... Convert to only HTML tags without any style on it.
"""

args = sys.argv
if len(args) >= 2:
    if(args[1].startswith('-')):
        if(args[1] == "-help" or args[1] == "--help"):
            print(HELP_TEXT)
    else:
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
        if "-open" in args:
            webbrowser.open(f"file://{os.path.realpath(htmlFileName)}")
else:
    print("\nUsage: abstractmark [abstractmark file] [abstractmark options] [args]\n\nSee \"abstractmark --help\" for more.\n")