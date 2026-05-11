from .lexer import *
from .astgen import *
from .hlog import *
from .compiler import *
import os
import types
import inspect

def load_uis(folder: str, debug=False):
    try:
        from ..state import state
    except ImportError:
        class State:
            pass
        state = State()

    base_path = os.path.dirname(inspect.stack()[1].filename)
    target_path = os.path.join(base_path, folder)

    if not os.path.isdir(target_path):
        raise ValueError(f"Invalid UI folder: {target_path}")

    if not hasattr(state, "uis"):
        state.uis = {}

    uiLogger = Logger()

    for root, _, files in os.walk(target_path):
        for file in files:
            if not file.endswith(".ui"):
                continue

            full_path = os.path.join(root, file)

            with open(full_path, "r", encoding="utf-8") as f:
                contents = f.read()

            lexer.content = contents
            lexer.lines = contents.split("\n")

            AST = parser.parse(contents)
            if AST is None:
                continue

            comp = Compiler([AST])

            module_name = os.path.splitext(file)[0]
            module = types.ModuleType(module_name)

            exec(comp.code, module.__dict__)

            state.uis[module_name] = module

            if debug:
                uiLogger.print(AstView(AST))
                uiLogger.print_code(comp.code)
