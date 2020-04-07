
from typing import List, Union
from enum import Enum, auto
from functools import reduce
from ast import VarAST, NumAST, ProcAST, FuncCallAST, BeginAST, LetAST, AssignAST

AST = Union[NumAST, VarAST, ProcAST, FuncCallAST, BeginAST, LetAST, AssignAST]


class ValType(Enum):
    NUM = auto()
    INT = auto()
    FLOAT = auto()
    BOOL = auto()
    PROCEDURE = auto()


MACRO_LST = ["@add", "@sub", "@mul", "@div", "<", ">", "<=", ">=", "eqv?"]


def execute_macro(macro, val_lst):
    def add():
        return ValType.NUM, reduce(lambda x, y: x + y, [val[1] for val in val_lst])

    def sub():
        return ValType.NUM, reduce(lambda x, y: x - y, [val[1] for val in val_lst])

    def mul():
        return ValType.NUM, reduce(lambda x, y: x * y, [val[1] for val in val_lst])

    def div():
        return ValType.NUM, reduce(lambda x, y: x / y, [val[1] for val in val_lst])

    def lt():
        assert len(val_lst) == 2
        return ValType.BOOL, val_lst[0][1] < val_lst[1][1]

    def eqv():
        assert len(val_lst) == 2
        return ValType.BOOL, val_lst[0][1] == val_lst[1][1]

    switch = {
        "@add": add,
        "@sub": sum,
        "@mul": mul,
        "@div": div,
        "@<":   lt,
        "@eqv": eqv,
    }

    return switch[macro]()


def apply_env(var_name: str, env: List):
    if not env:
        print("apply_env, find {} error".format(var_name))
        exit()
    if env[0] == var_name:
        return env[1]
    else:
        return apply_env(var_name, env[2])


def value_of(ast: AST, env: List) -> (any, List):
    if type(ast) == NumAST:
        return (ValType.NUM, ast.num_val), env
    elif type(ast) == VarAST:
        return apply_env(ast.var_name, env), env
    elif type(ast) == ProcAST:
        return (ValType.PROCEDURE, ast.params, ast.body), env
    elif type(ast) == AssignAST:
        var_name = ast.var.var_name
        rhs_val, env = value_of(ast.rhs, env)
        nenv = [var_name, rhs_val, env]
        return None, nenv
    elif type(ast) == FuncCallAST:
        func_name = ast.var.var_name

        if func_name in MACRO_LST:  # macro call
            val_lst = []
            for arg in ast.args:
                val, _ = value_of(arg, env)
                val_lst.append(val)
            rst = execute_macro(func_name, val_lst)
        else:  # function call
            (val_type, params, body) = apply_env(func_name, env)
            nenv = env
            for i, param in enumerate(params):
                val, _ = value_of(ast.args[i], nenv)
                nenv = [param.var_name, val, nenv]
            rst, _ = value_of(body, nenv)
        return rst, env


def interpret(ast_vec: List[AST]):
    env = []
    for i, ast in enumerate(ast_vec):
        rst, env = value_of(ast, env)
        if rst is not None:
            print("Exp {} ==> {}".format(i+1, rst[1]))
