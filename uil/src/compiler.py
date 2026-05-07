from .core import AstNode

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
        print(line)
        line.update_indent()

    def generate(self,index=0):
        print(f"{index=}", self.content)
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

        for prog in asts:
            self._stmts(prog.stmts)
        print(self.code)
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
            case _:
                res =Line(self._expr(stmt))
                self.cur.insert(
                    res
                )
        self.cur=res

    def _expr(self, expr):
        if not isinstance(expr, AstNode):
            return expr
        match expr.node_type:
            case "BINOP":
                return left+expr.op+right
            case "LITERAL":
                return expr.value
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
                _call = f"{self._expr(expr.target)}({args})"
                if _hoisting is not False:
                    self.cur.insert(res:=Line(
                        f"{_hoisting}={_call}"
                    ))
                    self.cur=res
                    return _hoisting
                return _call
            case _:
                print("unknown", expr.node_type)
                return ""

    def _args(self, args):
        _res = ""
        for target, value in args:
            _res+=f"{target}"
            if value:
                _res+="={value}"
            _res+=","
        return _res[:-1]
