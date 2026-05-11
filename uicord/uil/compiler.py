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
            + (
                "\n"
                if not isinstance(self.next, EmptyScope)
                else ""
            ) + (
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

class EmptyScope(Scope):
    pass

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

    def _parse_scope(self, scope, stmts):
        self.cur.insert(scope)
        self.cur = scope
        self._stmts(stmts)

    def _insert_empty_scope(self):
        end_scope = EmptyScope()
        self.cur.insert(end_scope)
        end_scope.indent = self.cur.indent - 2
        self.cur = end_scope

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
            case "FORLOOP":
                scope = Scope(
                    f"for {self._expr(stmt.child)} in {self._expr(stmt.parent)}:"
                )
                self._parse_scope(scope, stmt.stmts)
                self._insert_empty_scope()
            case "IF":
                cond = self._expr(stmt.expr)
                scope = Scope(
                    f"if {cond}:"
                )
                self._parse_scope(scope, stmt.stmts)
                self._insert_empty_scope()
                for else_stmt in stmt.elses:
                    if not else_stmt.expr:
                        scope = Scope(
                            f"else:"
                        )
                    else:
                        cond = self._expr(else_stmt.expr)
                        scope = Scope(
                            f"elif {cond}:"
                        )
                    self._parse_scope(scope, else_stmt.stmts)
                    self._insert_empty_scope()
                
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
            (f"{param.target}={self._expr(param.default)}" if param.default else param.target)
            for param in params
        ])
    def _parse_fn(self, fn, _awaited=False):
        params = self._params(fn.params)
        awaited = _awaited or fn.asynchronous
        scope = Scope(
            f"{"async " if awaited else ""}def {fn.target}({params}):"
        )
        self._parse_scope(scope, fn.stmts)
        self._insert_empty_scope()

    def _parse_string(self, string):
        return '"'+string.replace('"', '\\"')+'"'
        
    def _expr(self, expr):
        if not isinstance(expr, AstNode):
            if isinstance(expr, list):
                return 
            return expr
        match expr.node_type:
            case "BINOP":
                left = self._expr(expr.left)
                right = self._expr(expr.right)
                return left+expr.op+right
            case "LITERAL":
                return self._expr(expr.value) if expr.value != "null" else "None"
            case "STR":
                return (expr.format or '') + self._parse_string(expr.value)
            case "ATTR":
                left = self._expr(expr.parent)
                right = self._expr(expr.child)
                return left+"."+right
            case "LIST":
                return '['+",".join([self._expr(e) for e in expr.values])+']'
            case "INDEXING":
                left = self._expr(expr.parent)
                right = self._expr(expr.child)
                return left+"["+right+"]"
            case "IFEXPR":
                left = self._expr(expr.left)
                right = self._expr(expr.right)
                expr = self._expr(expr.expr)

                return f"{left} if {expr} else {right}"
            case "LIST_COMP":
                res = f"[{self._expr(expr.expr)} for "
                res += self._expr(expr.target.child)
                res += " in "
                res += self._expr(expr.target.parent)

                if expr.cond:
                    res += f" if {self._expr(expr.cond)}"
                res += "]"
                return res
            case "CALL":
                _hoisting=False
                _args = []
                for arg in expr.args:
                    if arg.target == "gid":
                        _hoisting=arg.value.value.value
                        continue
                    _args.append(
                        (
                            self._expr(arg.target),
                            self._expr(
                                arg.value
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
            case "ARG":
                _res = ""
                
                if expr.target:
                    _res+=f"{self._expr(expr.target)}="
                _res+=f"{self._expr(expr.value)}"
                return _res
            case _:
                print("unknown", expr.node_type)
                return ""

    def _args(self, args):
        _res = ""
        for target, value in args:
            if target:
                _res+=f"{self._expr(target)}="
            _res+=f"{self._expr(value)}"
            _res+=","
        return _res[:-1]
