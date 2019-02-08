import ast


class EnvVisitor(ast.NodeVisitor):
    def __init__(self):
        self.optional_environment_variables = set()
        self.required_environment_variables = set()

    def parse_and_visit(self, body, filename=''):
        doc = ast.parse(body, filename=filename)
        return self.visit(doc)

    def visit_Call(self, call):
        is_getenv = False
        is_environ_get = False
        if isinstance(call.func, ast.Attribute):
            if call.func.attr == 'getenv':
                is_getenv = True
            elif call.func.attr == 'get':
                if isinstance(call.func.value, ast.Attribute) and call.func.value.attr == 'environ':
                    is_environ_get = True
                elif isinstance(call.func.value, ast.Name) and call.func.value.id == 'environ':
                    is_environ_get = True
        elif isinstance(call.func, ast.Name):
            if call.func.id == 'getenv':
                is_getenv = True
        if is_getenv:
            if len(call.args) >= 1 and isinstance(call.args[0], ast.Str):
                self.optional_environment_variables.add(ast.literal_eval(call.args[0]))
        elif is_environ_get:
            if len(call.args) >= 1 and isinstance(call.args[0], ast.Str):
                self.optional_environment_variables.add(ast.literal_eval(call.args[0]))
        self.generic_visit(call)

    def visit_Subscript(self, what):
        is_env_slice = False
        if isinstance(what.value, ast.Attribute) and what.value.attr == 'environ':
            is_env_slice = True
        elif isinstance(what.value, ast.Name) and what.value.id == 'environ':
            is_env_slice = True
        if is_env_slice:
            if isinstance(what.slice, ast.Index) and isinstance(what.slice.value, ast.Str):
                self.required_environment_variables.add(ast.literal_eval(what.slice.value))
        self.generic_visit(what)
