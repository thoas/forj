import ast
import re


def expr(code, context=None):
    """Eval a math expression and return the result"""
    if not context:
        context = {}
    code = code.format(**context)

    # An especial case for my own when using percents values.
    # TODO: Fail if you are not comparing same type value like "50 > 20%" haves to fail
    code = re.sub("%", "", code)

    expr = ast.parse(code, mode="eval")
    code_object = compile(expr, "<string>", "eval")

    return eval(code_object)
