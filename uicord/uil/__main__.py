from uil import *
import uil.compiler as cs
import sys

uiLogger = Logger()

with open(sys.argv[1]) as f:
    contents = f.read()
lexer.content=contents
lexer.lines = contents.split("\n")
# TODO: add argument parser
if "-db" in sys.argv:
    lexer.input(contents)
    print("\n".join([repr(a) for a in lexer]))
    sys.exit()
AST = parser.parse(contents)
if AST is None:
    sys.exit()

uiLogger.print(
    AstView(AST)
)
comp = cs.Compiler([AST])
(uiLogger.print_code(comp.code))
