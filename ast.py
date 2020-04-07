
from typing import List

class BaseAST:
    def display(self, indent):
        pass


class NumAST(BaseAST):
    def __init__(self, num_val):
        # self.num_type = type  # int float etc.
        self.num_val = num_val


class VarAST(BaseAST):
    def __init__(self, var_name: str):
        self.var_name = var_name
        # self.var_type = var_type


class BeginAST(BaseAST):
    def __init__(self, asts):
        """
        :param asts: list[BaseAST, ...]
        """
        self.asts = asts


class LetAST(BaseAST):
    def __init__(self, var_vec, exp_vec, body):
        """
        :param var_vec:
        :param exp_vec:
        :param body:
        """
        self.var_vec = var_vec
        self.exp_vec = exp_vec
        self.body = body


class AssignAST(BaseAST):
    def __init__(self, var: VarAST, rhs):
        """
        :param var: VarAST
        :param rhs:
        """
        self.var = var
        self.rhs = rhs


class ProcAST(BaseAST):
    def __init__(self, params: List[VarAST], body):
        """
        :param params:      list[VarAST, ...]
        :param body:        BaseAST
        """
        self.params = params
        self.body = body


class FuncCallAST(BaseAST):
    def __init__(self, var: VarAST, args):
        """
        :param func_name:   VarAST
        :param args:        List[BaseAST, ...]
        """
        self.var = var
        self.args = args




