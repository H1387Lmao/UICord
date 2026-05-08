from .core import *

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
)                                                     
def p_STMTEXPR(p):
    """
    stmt : expr
    """
    p[0]=p[1]


def p_STMTASSIGN(p):
    """
    stmt : expr EQ expr
    """
    p[0]=AstNode(
        "ASSIGN",
        target=p[1],
        value=p[3]
    )

def p_FNDECL(p):
    """
    expr : AT ID LPAREN params RPAREN scope
         | AT async ID LPAREN params RPAREN scope
    """
    offset=0
    if p[2]=="async":
        offset=1
    p[0]=AstNode(                                             
        "FNDECL",                                             
        target=p[2+offset],
        params=p[4+offset],
        stmts=p[6+offset],
        asynchronous=bool(offset)
    )

def p_STMTRET(p):
    """
    stmt : ARROW expr
    """
    p[0]=AstNode(
        "RETURN",
        value=p[2]
    )

def p_STMTCALL(p):                                        
    """
    call : expr LPAREN args RPAREN
    """
    p[0]=AstNode(                                             
        "CALL",
        target=p[1],
        args=p[3],
        awaited=False
    )

def p_IMPORT(p):
    """
    stmt : import import_name
         | import import_name as ID
    """
    p[0]=AstNode(                                             
        "IMPORT",
        target=p[2],
        alias = None if len(p)==3 else p[4]
    )

def p_FROM_IMPORT(p):
    """
    stmt : from import_name import IMPORTS
    """
    p[0]=AstNode(                                             
        "FROM_IMPORT",
        parent=p[2],
        targets=p[4]
    )

def p_IMPORTNAME(p):
    """
    import_name : ID
                | DOT import_name
    """
    p[0]="".join(p[1:])

def p_IMPORTS(p):
    """
    IMPORTS : ID
            | MULTIPLY
    """
    p[0]=p[1]

def p_AWAITCALL(p):
    """
    expr : await call
    """
    p[2].awaited=True
    p[0]=p[2]

def p_ATTACH(p):
    """
    ATTACH : ID LPAREN params RPAREN FARROW scope
    """
    p[0]=AstNode(             
        "ATTACH",
        target=p[1],
        params=p[3],
        stmts=p[6]                                        
    )

def p_INDEXING(p):
    """
    expr : expr LBRACKET expr RBRACKET
    """
    p[0] = AstNode(
        "INDEXING",
        parent=p[1],
        child=p[3]
    )

def p_empty(p):
    """
    empty :
    """
    p[0]=[]

def p_ARG(p):
    """
    arg : expr
        | ID COLON expr
    """
    default=None
    if len(p)==4:                                             
        default=p[3]
    p[0]=AstNode("ARG",
        target=p[1],
        default=default
    )                                                 

def p_ARGS(p):                                            
    """
    args : arg                                                 
         | empty
         | args COMMA arg
    """
    if len(p)==4:
        p[1].append(p[3])
        p[0]=p[1]
    else:
        if p[1]:
            p[0]=[p[1]]
        else:
            p[0]=p[1]

def p_PARAM(p):                                           
    """
    param : ID
          | ID EQ expr
    """                                                   
    default=None
    if len(p)==4:                                             
        default=p[3]
    p[0]=AstNode("PARAM",
        target=p[1],                                          
        default=default
    )

def p_PARAMS(p):                                          
    """
    params : param                                               
           | empty                                               
           | params COMMA param                           
    """
    if len(p)==4:                                             
        p[1].append(p[3])                                     
        p[0]=p[1]                                         
    else:
        if p[1]:
            p[0]=[p[1]]
        else:
            p[0]=p[1]
def p_ATTR(p):
    """
    attr : expr DOT ID
         | expr DCOLON ATTACH
    """                                                   
    p[0]=AstNode("ATTR",
        parent=p[1],
        child=p[3]                
    )

def p_EXPR(p):
    """
    expr : attr
         | call
         | ID
         | NUM
         | STR
         | expr PLUS expr
         | expr MINUS expr
         | expr MULTIPLY expr
         | expr DIVIDE expr
         | LPAREN expr RPAREN
         | LBRACKET args RBRACKET
    """
    if len(p)==4:
        if isinstance(p[1], AstNode):
            p[0]=AstNode("BINOP",
                left=p[1],
                op=p[2],
                right=p[3]
            )
        else:
            p[0]=p[2]
    else:                                                     
        if isinstance(p[1], AstNode):
            p[0]=p[1]
        else:
            p[0]=AstNode("LITERAL", value=p[1])

def p_STMTS(p):
    """
    stmts : stmts stmt                                          
          | stmt
    """
    if isinstance(p[1],list):
        p[1].extend(p[2:])
        p[0]=p[1]
    else:
        p[0]=[p[1]]

def p_SCOPE(p):                                           
    """
    scope : LBRACE stmts RBRACE
    """
    p[0]=p[2]

def p_PROG(p):
    """                                                   
    s : stmts
      | empty
    """                                                   
    p[0]=AstNode("PROG", stmts=p[1])

def p_error(t):
    print_error(t)
