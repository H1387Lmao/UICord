from .core import AstNode

class Compiler:
    def __init__(self, asts):
        self.code = ""
        self.scope=0
        self.fns={}

        for ast in asts:
            self.compile_stmts(ast.stmts)
    def compile_stmts(self, stmts):
        for stmt in stmts:
            self.compile_stmt(stmt)
    def compile_target(self, expr):
        match expr.node_type:
            case "LITERAL":
                self.code+=expr.value
            case "ATTR":
                self.compile_expr(expr.parent)
                self.code+="."
                self.compile_expr(expr.child)
            case _:
                print("not implemented", expr.node_type)
    def compile_params(self, params):
        for param in params:
            self.code+=param.target
            if param.default:
                self.code+="="
                self.compile_expr(param.default)
            self.code+=", "
        self.code=self.code.rstrip(", ")
    def compile_literal(self, literal):
        if isinstance(literal, list):
            self.code+="["
            [
                self.compile_expr(a) for a in literal
            ]
            self.code+="]"
            return
        elif literal is None:
            self.code+="None"
            return
        self.code+=literal
    def compile_expr(self, expr):
        if not isinstance(expr, AstNode):
            return self.compile_literal(expr)
        match expr.node_type:
            case "BINOP":
                self.compile_expr(expr.left)
                self.code+=expr.op
                self.compile_expr(expr.right)
            case "LITERAL":
                self.code+=expr.value
            case "CALL":
                if expr.awaited: self.code+=f"await "
                self.compile_target(expr.target)
                self.code+="("
                self.compile_delimited(expr.args, ", ", self.compile_expr)
                self.code+=")"
            case "STR":
                res = '"'+expr.value.replace('"','\\"')+'"'
                if expr.format:
                    res=expr.format+res
                self.code+=res
            case "FNDECL":
                self.fns[expr.target]=len(self.code)
                self.code+=f"def {expr.target}("
                self.compile_params(expr.params)
                self.code+="):\n"
                self.scope+=1
                self.compile_stmts(expr.stmts)
            case "ARG":
                self.compile_expr(expr.target)
                if expr.default:
                    self.code+="="
                    self.compile_expr(expr.default)
            case "ATTACH":
                #TODO: Make attach create an asynchronous function and reference in the code
                pass
            case "RETURN":
                self.code+="return "
                self.compile_expr(expr.value)
            case _:
                self.compile_target(expr)

    def compile_delimited(self, args, delimiter, fn):
        for arg in args:
            fn(arg)
            self.code+=delimiter
        self.code = self.code.rstrip(delimiter)
    def compile_stmt(self, stmt):
        self.code+="  "*self.scope
        match stmt.node_type:
            case "ASSIGN":
                self.compile_target(stmt.target)
                self.code+="="
                self.compile_expr(stmt.value)
            case _:
                self.compile_expr(stmt)
        self.code+="\n"
