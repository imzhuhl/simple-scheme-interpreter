
from enum import Enum, auto
from ast import AssignAST, VarAST, NumAST, ProcAST, FuncCallAST, BeginAST


class Token(Enum):
    NUMBER = auto()
    STRING = auto()
    BOOLEAN = auto()
    IDENTIFIER = auto()
    KW_DEFINE = auto()
    KW_LET = auto()
    KW_IN = auto()
    KW_BEGIN = auto()
    KW_IF = auto()
    KW_LAMBDA = auto()

    # ADD = 15
    # SUB = 16
    # MUL = 17
    # DIV = 18
    # LE = 19   # <=
    # LT = 20   # <
    # GE = 21   # >=
    # GT = 22   # >

    LPAREN = auto()
    RPAREN = auto()
    SEMICOLON = auto()
    EOF = auto()
    ERROR = auto()


class Lexer:
    def __init__(self, code_str):
        self.code = code_str + "\0"
        self.length = len(code_str)
        self.idx = 0
        self.tokens = []

    def is_legal_identifier(self, c, is_first_letter):
        """
        :param c:               one character
        :param is_first_letter: True if first letter, False if it is not
        :return: bool, c is a legel identifier or not
        legel identifier: [a-z | A-Z | _ ] {_ | ? | - | a-z | A-Z | 0-9}
        """
        if is_first_letter:
            return str.isalpha(c) or c == "_"
        else:
            return str.isalpha(c) or str.isdigit(c) or \
                   c == "_" or c == "?" or c == "-"

    def get_char(self):
        """
        :return current char and `idx` point to next char
        """
        cc = self.code[self.idx]
        self.idx += 1
        return cc

    def get_token(self):
        cc = self.get_char()
        while cc == " " or cc == "\n" or cc == "\t":
            cc = self.get_char()

        if self.is_legal_identifier(cc, True):
            id_name = cc
            cc = self.get_char()
            while self.is_legal_identifier(cc, False):
                id_name += cc
                cc = self.get_char()
            self.idx -= 1
            if id_name == "define":
                tk = (Token.KW_DEFINE, "define")
            elif id_name == "lambda":
                tk = (Token.KW_LAMBDA, "lambda")
            else:
                tk = (Token.IDENTIFIER, id_name)
        elif str.isdigit(cc):  # number
            num_val = cc
            cc = self.get_char()
            while str.isdigit(cc) or cc == ".":
                num_val += cc
                cc = self.get_char()
            self.idx -= 1
            tk = (Token.NUMBER, num_val)
        elif cc == "(":
            tk = (Token.LPAREN, "(")
        elif cc == ")":
            tk = (Token.RPAREN, ")")
        elif cc == "+":
            tk = (Token.IDENTIFIER, "@add")
        elif cc == "-":
            tk = (Token.IDENTIFIER, "@sub")
        elif cc == "*":
            tk = (Token.IDENTIFIER, "@mul")
        elif cc == "/":
            tk = (Token.IDENTIFIER, "@div")
        elif cc == ";":
            while self.get_char() != "\n":
                pass
            tk = (Token.SEMICOLON, ";")
        elif cc == "\0":
            tk = (Token.EOF, "\0")
        else:
            print("Not support yet")
            exit(0)
        return tk

    def do_lex(self):
        tk = self.get_token()
        while tk[0] != Token.EOF:
            self.tokens.append(tk)
            tk = self.get_token()
        return self.tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = 0
        self.switch = {  # only used by parse_expression function
            Token.KW_DEFINE:    self.parse_define,
            Token.KW_LAMBDA:    self.parse_lambda,
            Token.KW_BEGIN:     self.parse_begin,
            Token.KW_LET:       self.parse_let,
            Token.KW_IF:        self.parse_if,
            Token.IDENTIFIER:   self.parse_func_call,
        }

    def verify_code(self):
        """
        only verify parentheses `(` and `)`
        """
        lnum, rnum = 0, 0
        for token in self.tokens:
            if token[0] == Token.LPAREN:
                lnum += 1
            elif token[0] == Token.RPAREN:
                rnum += 1
        if lnum != rnum:
            print("verify code error")
            exit(0)

    def parse_var(self):
        return VarAST(self.tokens[self.idx][1])

    def parse_num(self):
        num_str = self.tokens[self.idx][1]
        # temporary simple treatment
        num_val = float(num_str) if "." in num_str else int(num_str)
        return NumAST(num_val)

    def parse_define(self):
        # assert self.tokens[self.idx][0] == Token.KW_DEFINE
        self.idx += 1
        # assert self.tokens[self.idx][0] == Token.IDENTIFIER
        var_name = self.tokens[self.idx][1]
        var_ast = self.parse_var()
        self.idx += 1

        if self.tokens[self.idx][0] == Token.LPAREN:
            # func define, parse `lambda` expression
            # `( lambda .... )`
            self.idx += 1
            lhs = self.parse_lambda()
        # some value or other variable
        elif self.tokens[self.idx][0] == Token.NUMBER:
            lhs = self.parse_num()
        else:   # Token.IDENTIFIER:
            lhs = self.parse_var()

        self.idx += 1
        assert self.tokens[self.idx][0] == Token.RPAREN  # close define
        return AssignAST(var_ast, lhs)

    def parse_lambda(self) -> ProcAST:
        assert self.tokens[self.idx][0] == Token.KW_LAMBDA
        self.idx += 1

        # parse parameters
        assert self.tokens[self.idx][0] == Token.LPAREN
        param_lst = []
        self.idx += 1
        while self.tokens[self.idx][0] != Token.RPAREN:
            assert self.tokens[self.idx][0] == Token.IDENTIFIER
            var_ast = self.parse_var()
            param_lst.append(var_ast)
            self.idx += 1

        self.idx += 1
        assert self.tokens[self.idx][0] == Token.LPAREN
        body = self.parse_expression()
        assert self.tokens[self.idx][0] == Token.RPAREN
        self.idx += 1

        assert self.tokens[self.idx][0] == Token.RPAREN
        return ProcAST(param_lst, body)

    def parse_func_call(self):
        assert self.tokens[self.idx][0] == Token.IDENTIFIER
        var_ast = self.parse_var()  # an ast include function name
        args = []
        self.idx += 1
        while self.tokens[self.idx][0] != Token.RPAREN:
            args.append(self.parse_expression())
            self.idx += 1

        return FuncCallAST(var_ast, args)

    def parse_begin(self):
        # assert self.tokens[self.idx][0] == Token.KW_BEGIN

        begin_ast = []
        self.idx += 1
        # I want a `)` to match `(begin ...` to end begin expression
        while self.tokens[self.idx][0] != Token.RPAREN:
            begin_ast.append(self.parse_expression())
            self.idx += 1

        assert self.tokens[self.idx][0] == Token.RPAREN  # close (begin ...)

        return BeginAST(begin_ast)

    def parse_let(self):
        pass

    def parse_if(self):
        pass

    def parse_expression(self):
        if self.tokens[self.idx][0] == Token.IDENTIFIER:
            return self.parse_var()
        elif self.tokens[self.idx][0] == Token.NUMBER:
            return self.parse_num()

        # else it is a `( expression )`
        assert self.tokens[self.idx][0] == Token.LPAREN
        self.idx += 1

        tk = self.tokens[self.idx][0]
        rst_ast = self.switch[tk]()

        assert self.tokens[self.idx][0] == Token.RPAREN
        return rst_ast

    def do_parse(self):
        rst_ast = []
        while self.idx < len(self.tokens):
            if self.tokens[self.idx][0] == Token.IDENTIFIER:
                rst_ast.append(self.parse_var())
            elif self.tokens[self.idx][0] == Token.NUMBER:
                rst_ast.append(self.parse_num())
            elif self.tokens[self.idx][0] == Token.LPAREN:
                rst_ast.append(self.parse_expression())
            self.idx += 1
        return rst_ast


def main():
    file_path = "./example_file/example01"
    with open(file_path, "r") as f:
        code_str = f.read()
    lex = Lexer(code_str)
    tokens = lex.do_lex()
    # print(tokens)
    parser = Parser(tokens)

    ast_vec = parser.do_parse()

    from interpreter import interpret
    interpret(ast_vec)


if __name__ == '__main__':
    main()
