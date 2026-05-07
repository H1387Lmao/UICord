from .core import AstNode
from .rules import *
from .lrules import *
import ply.yacc as yacc

parser = yacc.yacc(start="s")
