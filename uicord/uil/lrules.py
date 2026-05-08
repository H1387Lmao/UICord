import re
from .core import AstNode

kwrds=("await", "async", "import", "from", "as")

RULES = {
    r"\+": "PLUS",
    "-": "MINUS",
    "/": "DIVIDE",
    r"\*": "MULTIPLY",
    "@": "AT",
    ",": "COMMA",
    "=": "EQ",
    r"\.": "DOT",
    ":": "COLON",
    "::": "DCOLON",
    "->": "ARROW",
    "=>": "FARROW",
    (r"\(", r"\)"): ("LR", "PAREN"),
    (r"\{", r"\}"): ("LR", "BRACE"),
    (r"\[", r"\]"): ("LR", "BRACKET")
}

tokens = [
    "ID", "NUM", "STR",
    *kwrds
]

for rule, token_name in RULES.items():
    if isinstance(rule, str):
        exec(f"t_{token_name} = r\"{rule}\"")
        tokens.append(token_name)
        continue
    for i, c in enumerate(rule):
        di, name = token_name
        exec(f"t_{di[i]}{name} = r\"{c}\"")
        tokens.append(di[i]+name)

def t_STR(t):
    r'[frb]?"[^"]*"'
    t.value=AstNode(
        "STR",
        value=t.value.split('"')[1],
        format=t.value[0] if t.value[0] != '"' else None
    )
    return t

def t_ID(t):
    r"[A-Za-z_]+\w*"
    if t.value in kwrds:
        t.type=t.value
    return t

t_NUM=r"\d+(\.(\d+)?)?"

def t_error(c):
    # TODO: add actual error
    print("wtf is this:", c)

def t_COMMENT(_):
    r"//.*"
    
def t_NEWLINE(t):
    r"\n+"
    t.lexer.lineno+=len(t.value)
    
t_ignore="\t "
