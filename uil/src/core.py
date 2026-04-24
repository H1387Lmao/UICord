import sys
from .hlog import Logger

error_logger = Logger()


def AstView(node, prefix="", is_last=True, ITEM_NAME=None):
    if not isinstance(node, AstNode):
        return ""
    res = prefix
    name = ITEM_NAME+": " if ITEM_NAME is not None else ""
    if prefix:
        res += f"[dark gray]└── [?]" if is_last else f"[dark Gray]├── [?]"
    res += f"[gold]{name}Ast({node.node_type})[?]\n"

    print(name)
    child_prefix = prefix + ("    " if is_last else f"[dark Gray]│   [?]")

    items = [(k, v) for k, v in node.__dict__.items() if k != "node_type"]

    for i, (k, v) in enumerate(items):
        last = i == len(items) - 1

        if isinstance(v, AstNode):
            res += AstView(v, child_prefix, last, ITEM_NAME=k)

        elif isinstance(v, list):
            res += child_prefix
            res += f"[dark Gray]└── [?]" if last else f"[dark Gray]├── [?]"
            res += f"[blue]{k} (List) \n[?]"

            for j, item in enumerate(v):
                res += AstView(
                    item,
                    child_prefix + ("    " if last else f"[dark Gray]│   [?]"),
                    j == len(v) - 1,
                )

        else:
            res += child_prefix
            res += f"[dark Gray]└── [?]" if last else f"[dark Gray]├── [?]"
            if isinstance(v, str):
                color = "[green]"
            elif isinstance(v, bool):
                color = "[red]"
            elif isinstance(v, int):
                color = "[purple]"
            else: color=""
            res += f"{k}: {color}{repr(v)}\n[?]"
    return res

class AstNode:
    def __init__(
        self,
        node_type,
        **kwargs
    ):
        self.node_type=node_type
        [setattr(self, a, b)
            for a, b in kwargs.items()
        ]

def find_column(input_text, token):
    last_cr = input_text.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = -1
    return token.lexpos - last_cr

def print_error(token):
    full_text = token.lexer.lexdata
    line = token.lexer.lines[token.lineno - 1]

    col = find_column(full_text, token)

    expanded = line.replace("\t", "  ")
    stripped = expanded.lstrip()

    leading_ws = len(expanded) - len(stripped)
    col -= leading_ws

    error_logger.print('[Pink]Unexpected token: `' + str(token.value) + '`')
    error_logger.print(f"[Red]At Line {token.lineno}")
    error_logger.print_code(stripped)

    caret_pos = max(col, 1)
    error_logger.print(" " * (caret_pos - 1) + "^" * len(str(token.value)))

    sys.exit()
