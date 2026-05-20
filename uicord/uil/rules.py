from .core import *

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQEQ', 'MEQ', 'LEQ', 'LESS', 'MORE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
)

def p_STMTEXPR(p):
    """
    stmt : expr
    """
    p[0] = p[1]

def p_STMTASSIGN(p):
    """
    stmt : expr EQ expr
    """
    p[0] = AstNode(
        "ASSIGN",
        target=p[1],
        value=p[3]
    )

def p_FNDECL(p):
    """
    expr : AT ID LPAREN params RPAREN scope
         | AT async ID LPAREN params RPAREN scope
    """
    offset = 1 if p[2] == "async" else 0

    p[0] = AstNode(
        "FNDECL",
        target=p[2 + offset],
        params=p[4 + offset],
        stmts=p[6 + offset],
        asynchronous=bool(offset)
    )

def p_FORLOOP_HEADER(p):
    """
    fl_header : for expr in expr
    """
    p[0] = AstNode(
        "FORLOOP",
        child=p[2],
        parent=p[4]
    )

def p_FORLOOP(p):
    """
    stmt : fl_header scope
    """
    p[1].stmts = p[2]
    p[0]=p[1]

def p_LISTCOMPREHENSION(p):
    """
    expr : LBRACKET expr fl_header RBRACKET
         | LBRACKET expr fl_header if expr RBRACKET
    """
    p[0]=AstNode(
        "LIST_COMP",
        expr=p[2],
        target=p[3],
        cond=p[5] if len(p)==7 else None
    )

def p_IFEXPR(p):
    """
    expr : if expr COLON expr else expr
    """

    p[0]=AstNode(
        "IFEXPR",
        left=p[4],
        expr=p[2],
        right=p[6]
    )

def p_ELSE(p):
    """
    else_part : else scope
              | else if expr scope
    """
    p[0] = AstNode(
        "ELSE",
        expr=None if len(p) == 3 else p[3],
        stmts=p[2] if len(p) == 3 else p[4]
    )

def p_ELSES(p):
    """
    elses : elses else_part
          | else_part
    """
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

def p_STMTRET(p):
    """
    stmt : ARROW expr
    """
    p[0] = AstNode(
        "RETURN",
        value=p[2]
    )

def p_STMTCALL(p):
    """
    call : expr LPAREN args RPAREN
    """
    p[0] = AstNode(
        "CALL",
        target=p[1],
        args=p[3],
        awaited=False
    )

def p_IF_STMT(p):
    """
    stmt : if expr scope elses
         | if expr scope
    """
    p[0] = AstNode(
        "IF",
        expr=p[2],
        stmts=p[3],
        elses=p[4] if len(p) == 5 else []
    )

def p_IMPORT(p):
    """
    stmt : import import_name
         | import import_name as ID
    """
    p[0] = AstNode(
        "IMPORT",
        target=p[2],
        alias=None if len(p) == 3 else p[4]
    )

def p_FROM_IMPORT(p):
    """
    stmt : from import_name import imports
    """
    p[0] = AstNode(
        "FROM_IMPORT",
        parent=p[2],
        targets=p[4]
    )

def p_IMPORTNAME(p):
    """
    import_name : ID
                | DOT import_name
    """
    p[0] = "".join(map(str, p[1:]))

def p_IMPORTS(p):
    """
    imports : ID
            | MULTIPLY
    """
    p[0] = p[1]

def p_AWAITCALL(p):
    """
    expr : await call
    """
    p[2].awaited = True
    p[0] = p[2]

def p_ATTACH(p):
    """
    ATTACH : ID LPAREN params RPAREN FARROW scope
    """
    p[0] = AstNode(
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
    p[0] = None

def p_ARG(p):
    """
    arg : expr
        | ID COLON expr
    """
    if len(p) == 2:
        p[0] = AstNode(
            "ARG",
            target=None,
            value=p[1]
        )
    else:
        p[0] = AstNode(
            "ARG",
            target=p[1],
            value=p[3]
        )

def p_ARGS(p):
    """
    args : arg
         | empty
         | args COMMA arg
    """
    if len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [] if p[1] is None else [p[1]]

def p_PARAM(p):
    """
    param : ID
          | ID EQ expr
    """
    p[0] = AstNode(
        "PARAM",
        target=p[1],
        default=None if len(p) == 2 else p[3]
    )

def p_PARAMS(p):
    """
    params : param
           | empty
           | params COMMA param
    """
    if len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [] if p[1] is None else [p[1]]

def p_ATTR(p):
    """
    attr : expr DOT ID
         | expr DCOLON ATTACH
    """
    p[0] = AstNode(
        "ATTR",
        parent=p[1],
        child=p[3]
    )

def p_CONDITION(p):
    """
    condition : expr EQEQ expr
              | expr MEQ expr
              | expr LEQ expr
              | expr LESS expr
              | expr MORE expr
              | expr OR expr
              | expr AND expr
    """
    if p[2]=="||": p[2]=" or "
    if p[2]=="&&": p[2]=" and "
    p[0] = AstNode(
        "BINOP",
        left=p[1],
        op=p[2],
        right=p[3]
    )

def p_LIST(p):
    """
    expr : LBRACKET args RBRACKET
    """
    p[0] = AstNode(
        "LIST",
        values=p[2]
    )

def p_GROUP(p):
    """
    expr : LPAREN expr RPAREN
    """
    p[0] = p[2]

def p_BINOP(p):
    """
    expr : expr PLUS expr
         | expr MINUS expr
         | expr MULTIPLY expr
         | expr DIVIDE expr
    """
    p[0] = AstNode(
        "BINOP",
        left=p[1],
        op=p[2],
        right=p[3]
    )

def p_LITERAL(p):
    """
    expr : ID
         | NUM
         | STR
    """
    p[0] = AstNode(
        "LITERAL",
        value=p[1]
    )

def p_EXPR_FORWARD(p):
    """
    expr : attr
         | call
         | condition
    """
    p[0] = p[1]

def p_STMTS(p):
    """
    stmts : stmts stmt
          | stmt
    """
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

def p_SCOPE(p):
    """
    scope : LBRACE stmts RBRACE
    """
    p[0] = p[2]

def p_PROG(p):
    """
    s : stmts
      | empty
    """
    p[0] = AstNode(
        "PROG",
        stmts=[] if p[1] is None else p[1]
    )

def p_error(t):
    print_error(t)
