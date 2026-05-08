from .core import AstNode
import random

class Line:
    def __init__(
            self,
            content,
            previous=None
    ):
        self.prev = previous
        self.next = None
        self.content = content
    def __repr__(self):
        return self.content
    def update_indent(self):
        self.indent = (
            self.prev.indent+1
            if isinstance(
                self.prev, Scope
            )
            else
            self.prev.indent
        ) if self.prev else 0

    def insert(self, line):
        if self.next:
            self.next.prev = line
        
        line.next = self.next
        self.next = line
        line.prev = self
        line.update_indent()
    def insert_before(self, line):
        if isinstance(line, Scope):
            self.indent+=1

        line.next = self
        line.prev = self.prev
        self.prev.next = line
        self.prev = line
        line.update_indent()

    def generate(self,index=0):
        return (
            "  "*self.indent + self.content \
            + "\n" + (
                self.next.generate(index+1)
                if self.next is not None
                else ""
            )
        )

class Scope(Line):
    def __init__(
            self, content="",
            previous=None,
            indent=-1
    ):
        self.indent=indent

        super().__init__(content, previous)

class Compiler:
    def __init__(self, asts):
        self.code = Scope()
        
        self.cur = self.code

        self.lamdba_count = 0

        for prog in asts:
            self._stmts(prog.stmts)
        self.code=self.code.generate()

    def _stmts(self, stmts):
        for stmt in stmts:
            self._stmt(stmt)

    def _stmt(self, stmt):
        match stmt.node_type:
            case "ASSIGN":
                value = self._expr(stmt.value)
                target = self._expr(stmt.target)
                self.cur.insert(
                    res:=Line(f"{target}={value}")
                )
            case "RETURN":
                value = self._expr(stmt.value)
                res = Line(f"return {value}")
                self.cur.insert(
                    res
                )
            case "FNDECL":
                self._parse_fn(stmt)
            case "FROM_IMPORT":
                res = Line(f"from {stmt.parent} import {stmt.targets}")
                self.cur.insert(
                    res
                )
            case "IMPORT":
                alias = "" if not stmt.alias else f" as {stmt.alias}"
                res = Line(f"import {stmt.target}{alias}")
                self.cur.insert(
                    res
                )
            case _:
                res = Line(self._expr(stmt))
                self.cur.insert(
                    res
                )
        try:
            self.cur=res
        except:
            pass
    def _params(self, params):
        return ",".join([
            (f"{param.target}={param.default}" if param.default else param.target)
            for param in params
        ])
    def _parse_fn(self, fn, _awaited=False):
        params = self._params(fn.params)
        awaited = _awaited or fn.asynchronous
        scope = Scope(
            f"{"async " if awaited else ""}def {fn.target}({params}):"
        )
        self.cur.insert(scope)
        self.cur = scope

        self._stmts(fn.stmts)
        
        end_scope = Scope()
        
        self.cur.insert(end_scope)
        end_scope.indent-=2
        self.cur = end_scope
        
    def _expr(self, expr):
        if not isinstance(expr, AstNode):
            return expr
        match expr.node_type:
            case "BINOP":
                return left+expr.op+right
            case "LITERAL":
                return expr.value if expr.value != "null" else "None"
            case "STR":
                return repr(expr.value)
            case "ATTR":
                left = self._expr(expr.parent)
                right = self._expr(expr.child)
                return left+"."+right
            case "CALL":
                _hoisting=False
                _args = []
                for arg in expr.args:
                    if arg.target == "gid":
                        _hoisting=arg.default.value
                        continue
                    _args.append(
                        (
                            self._expr(arg.target),
                            self._expr(
                                arg.default
                            )
                        )
                    )
                args = self._args(_args)
                awaited = "await " if expr.awaited else ""
                _call = f"{awaited}{self._expr(expr.target)}({args})"
                if _hoisting is not False:
                    self.cur.insert(res:=Line(
                        f"{_hoisting}={_call}"
                    ))
                    self.cur=res
                    return _hoisting
                return _call
            case "FNDECL":
                self._parse_fn(expr)
                return expr.target
            case "ATTACH":
                target=expr.target
                expr.target = f"lambda_{self.lamdba_count}"
                self.lamdba_count+=1
                self._parse_fn(expr, True)
                return f"{target}({expr.target})"
            case _:
                print("unknown", expr.node_type)
                return ""

    def _args(self, args):
        _res = ""
        for target, value in args:
            _res+=f"{target}"
            if value:
                _res+=f"={value}"
            _res+=","
        return _res[:-1]
