from .core import AstNode
class Compiler:
    def __init__(self, asts):
        self.scopes=[[""]]
        self.fns={}

        for ast in asts:
            self.compile_stmts(ast.stmts)
    def add_code(self, code, line_target=0):
        self.scopes[-1][-1 + line_target] += code
    def add_line(self, line_target=0):
        self.scopes[-1].insert(
            len(self.scopes[-1])-line_target,
            ""
        )
    def indent(self):
        self.add_code("  "*(len(self.scopes)-1))
    def compile_stmts(self, stmts):
        for stmt in stmts:
            self.compile_stmt(stmt)
    @property
    def code(self):
        return "\n".join(self.scopes[-1])
    def compile_target(self, expr, indent=False):
        if indent:
            self.indent()
        match expr.node_type:
            case "LITERAL":
                self.add_code(expr.value)
            case "ATTR":
                self.compile_expr(expr.parent)
                self.add_code(".")
                self.compile_expr(expr.child)
            case "STR":
                self.add_code(expr.value)
            case _:
                print("not implemented", expr.node_type)
    def compile_params(self, params):
        for param in params:
            self.add_code(param.target)
            if param.default:
                self.add_code("=")
                self.compile_expr(param.default)
            self.add_code(", ")
        self.scopes[-1][-1]=self.scopes[-1][-1].rstrip(", ")
    def compile_literal(self, literal):
        if isinstance(literal, list):
            self.add_code("[")
            [
                self.compile_expr(a) for a in literal
            ]
            self.add_code("]")
            return
        elif literal is None:
            self.add_code("None")
            return
        self.add_code(literal)
    def extract_call(self, call_expr):
        for arg in call_expr.args:
            if arg.node_type == "ARG" and arg.target == "id":
                return arg.default.value
        return None
    def extract_calls_recursive(self, expr):
        extracted = []
    
        if not isinstance(expr, AstNode):
            return expr, extracted
        if getattr(expr, "_extracted", False):
            return expr, extracted
    
        if expr.node_type == "CALL":
            name = self.extract_call(expr)
            if name:
                expr._extracted=True
                new_args = []
                for arg in expr.args:
                    new_arg, sub = self.extract_calls_recursive(arg)
                    extracted.extend(sub)
                    new_args.append(new_arg)
    
                expr.args = new_args
                extracted.append((name, expr))
                return name, extracted
    
        for attr in vars(expr):
            val = getattr(expr, attr)
    
            if isinstance(val, AstNode):
                new_val, sub = self.extract_calls_recursive(val)
                setattr(expr, attr, new_val)
                extracted.extend(sub)
    
            elif isinstance(val, list):
                new_list = []
                for item in val:
                    if isinstance(item, AstNode):
                        new_item, sub = self.extract_calls_recursive(item)
                        extracted.extend(sub)
                        new_list.append(new_item)
                    else:
                        new_list.append(item)
                setattr(expr, attr, new_list)
    
        return expr, extracted
    def compile_expr(self, expr):
        if not isinstance(expr, AstNode):
            return self.compile_literal(expr)
        match expr.node_type:
            case "BINOP":
                self.compile_expr(expr.left)
                self.add_code(expr.op)
                self.compile_expr(expr.right)
            case "LITERAL":
                self.add_code(expr.value)
            case "CALL":
                expr, extracted = self.extract_calls_recursive(expr)
                
                for name, value in extracted:
                    self.add_code(f"  {name} = ")
                    self.compile_expr(value)
                    self.add_line()
                if not getattr(expr, "_extracted", False):
                    self.indent()
                    
                self.compile_target(expr.target)
                self.add_code("(")
                
                for arg in expr.args:
                    if isinstance(arg, str):
                        self.add_code(arg)
                    else:
                        self.compile_expr(arg)
                    self.add_code(", ")
            
                self.scopes[-1][-1] = self.scopes[-1][-1].rstrip(", ")
                self.add_code(")")
            case "STR":
                res = '"'+expr.value.replace('"','\\"')+'"'
                if expr.format:
                    res=expr.format+res
                self.add_code(res)
            case "FNDECL":
                self.fns[expr.target]=len(self.scopes[-1])
                self.add_code(f"def {expr.target}(")
                self.compile_params(expr.params)
                self.add_code("):")
                self.add_line()
                
                self.scopes.append([""])
                self.compile_stmts(expr.stmts)

                body = self.scopes.pop()
                self.scopes[-1].extend(body)
            case "ARG":
                if isinstance(expr.target, str) and expr.target =="id":
                    return
                else:
                    self.compile_expr(expr.target)
                if expr.default:
                    self.add_code("=")
                    self.compile_expr(expr.default)
            case "ATTACH":
                #TODO: Make attach create an asynchronous function and reference in the code
                print("not implemented attach")
            case "RETURN":
                self.add_code("return ")
                self.compile_expr(expr.value)
            case _:
                self.compile_target(expr)
    def compile_delimited(self, args, delimiter, fn):
        for arg in args:
            fn(arg)
            self.add_code(delimiter)
        self.scopes[-1][-1] = self.scopes[-1][-1].rstrip(delimiter)
    def compile_stmt(self, stmt):
        match stmt.node_type:
            case "ASSIGN":
                self.indent()
                self.compile_target(stmt.target)
                self.add_code("=")
                self.compile_expr(stmt.value)
                self.add_line()
            case _:
                self.indent()
                self.compile_expr(stmt)
        self.add_line()
