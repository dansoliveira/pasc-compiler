from enum import Enum


class InfIdentificador:
    def __init__(self):
        self.info = ""


class Token:

    def __init__(self, classe, lexema):
        self.__classe = classe
        self.lexema = lexema

    def formata_token_print(self, linha, coluna):
        return '<{},"{}"> linha: {} | coluna: {}'.format(self.classe.name, self.lexema, linha, coluna)

    @property
    def classe(self):
        return self.__classe

    @classe.setter
    def classe(self, classe):
        self.__classe = classe


class TabelaDeSimbolos:

    def __init__(self):
        self.tabela_de_simbolos = {Token(Tipo.KW, "program"): InfIdentificador()
                                   Token(Tipo.KW, "if"): InfIdentificador(),
                                   Token(Tipo.KW, "else"): InfIdentificador(),
                                   Token(Tipo.KW, "while"): InfIdentificador(),
                                   Token(Tipo.KW, "write"): InfIdentificador(),
                                   Token(Tipo.KW, "read"): InfIdentificador(),
                                   Token(Tipo.KW, "num"): InfIdentificador(),
                                   Token(Tipo.KW, "char"): InfIdentificador(),
                                   Token(Tipo.KW, "not"): InfIdentificador(),
                                   Token(Tipo.KW, "or"): InfIdentificador(),
                                   Token(Tipo.KW, "and"): InfIdentificador()}

    def add(self, token, inf_identificador):
        self.tabela_de_simbolos[token] = inf_identificador

    def retorna_token(self, lexema):
        for token in self.tabela_de_simbolos.keys():
            if token.lexema == lexema:
                return token

        return None

    def imprime_ts(self):
        for token in self.tabela_de_simbolos.keys():
            print("<{}, {}>".format(token.classe, token.lexema))

class Tipo(Enum):
    EOF = -1

    CON_NUM = 0
    CON_CHAR = 1
    LIT = 2
    ID = 3

    SMB_SEM = 4
    SMB_COM = 5
    SMB_CPA = 6
    SMB_OPA = 7
    SMB_CBC = 8
    SMB_OBC = 9

    OP_ASS = 10
    OP_EQ = 11
    OP_DIV = 12
    OP_MUL = 13
    OP_MIN = 14
    OP_AD = 15
    OP_LE = 16
    OP_LT = 17
    OP_GE = 18
    OP_GT = 19
    OP_NE = 20

    KW = 21
