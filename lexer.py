from lexer_tools import *

class Lexer():
    caracs_especiais = {"\r": "Carro de retorno", "\n": "Quebra de linha", "\b": "Espaço em branco", "\t": "Tabulação",
                        " ": "Espaço em branco"}

    EOF = ""
    linha = 1
    coluna = 1
    coluna_inicial = 1
    carac = ''
    carac_decoded = ''
    num_estado = 0
    lexema = []
    tabela_de_simbolos = TabelaDeSimbolos()
    arquivo = open("teste_pasc2_erro.psc", "rb")

    def q0(self):
        if self.carac_decoded is self.EOF:
            return Token(Tipo.EOF, "EOF")
        elif self.carac_decoded is "\n":
            self.linha += 1
            self.coluna = 1
            self.coluna_inicial = 1
        elif self.carac_decoded is " ":
            self.coluna += 1
        elif self.carac_decoded is "\t":
            self.coluna += 3
        elif self.carac_decoded.isdigit():
            self.coluna_inicial = self.coluna
            self.coluna += 1
            self.num_estado = 1
            self.lexema.append(self.carac_decoded)
        elif self.carac_decoded is "'":
            self.coluna_inicial = self.coluna
            self.coluna += 1
            self.num_estado = 5
            self.lexema.append(self.carac_decoded)
        elif self.carac_decoded is '"':
            self.coluna_inicial = self.coluna
            self.coluna += 1
            self.num_estado = 8
            self.lexema.append(self.carac_decoded)
        elif self.carac_decoded.isalpha():
            self.coluna_inicial = self.coluna
            self.coluna += 1
            self.num_estado = 11
            self.lexema.append(self.carac_decoded)
        elif self.carac_decoded is ";":
            self.coluna_inicial = self.coluna
            self.coluna += 1
            return Token(Tipo.SMB_SEM, ";")
        elif self.carac_decoded is ",":
            self.coluna_inicial = self.coluna
            self.coluna += 1
            return Token(Tipo.SMB_COM, ",")
        elif self.carac_decoded is ")":
            self.coluna_inicial = self.coluna
            self.coluna += 1
            return Token(Tipo.SMB_CPA, ")")
        elif self.carac_decoded is "(":
            self.coluna_inicial = self.coluna
            self.coluna += 1
            return Token(Tipo.SMB_OPA, "(")
        elif self.carac_decoded is "}":
            self.coluna_inicial = self.coluna
            self.coluna += 1
            return Token(Tipo.SMB_CBC, "}")
        elif self.carac_decoded is "{":
            self.coluna_inicial = self.coluna
            self.coluna += 1
            return Token(Tipo.SMB_OBC, "{")
        elif self.carac_decoded is "=":
            self.coluna_inicial = self.coluna
            self.coluna += 1
            self.num_estado = 19
        elif self.carac_decoded is "/":
            self.coluna_inicial = self.coluna
            self.coluna += 1
            self.num_estado = 22
        elif self.carac_decoded is "*":
            self.coluna_inicial = self.coluna
            self.coluna += 1
            return Token(Tipo.OP_MUL, "*")
        elif self.carac_decoded is "-":
            self.coluna_inicial = self.coluna
            self.coluna += 1
            return Token(Tipo.OP_MIN, "-")
        elif self.carac_decoded is "+":
            self.coluna_inicial = self.coluna
            self.coluna += 1
            return Token(Tipo.OP_AD, "+")
        elif self.carac_decoded is "<":
            self.coluna_inicial = self.coluna
            self.coluna += 1
            self.num_estado = 31
        elif self.carac_decoded is ">":
            self.coluna_inicial = self.coluna
            self.coluna += 1
            self.num_estado = 34
        elif self.carac_decoded is "!":
            self.coluna_inicial = self.coluna
            self.coluna += 1
            self.num_estado = 37

        return None

    def q1(self):
        self.coluna += 1
        if self.carac_decoded.isdigit():
            self.num_estado = 1
            self.lexema.append(self.carac_decoded)
        elif self.carac_decoded is ".":
            self.num_estado = 2
            self.lexema.append(self.carac_decoded)
        else:
            self.retorna_ponteiro()
            #tkn = self.tabela_de_simbolos.retorna_token(''.join(self.lexema))

            #if tkn is None:
            return Token(Tipo.CON_NUM, ''.join(self.lexema))

            #return tkn

        return None

    def q2(self):
        self.coluna += 1
        if self.carac_decoded.isdigit():
            self.num_estado = 3
            self.lexema.append(self.carac_decoded)
        else:
            self.sinaliza_erro("[Q2]Caractere '{}' inválido. É esperado um dígito.".format(self.carac_decoded), self.linha, self.coluna)

        return None

    def q3(self):
        self.coluna += 1
        if self.carac_decoded.isdigit():
            self.num_estado = 3
            self.lexema.append(self.carac_decoded)
        else:
            self.retorna_ponteiro()
            #tkn = self.tabela_de_simbolos.retorna_token(''.join(self.lexema))

            #if tkn is None:
            return Token(Tipo.CON_NUM, ''.join(self.lexema))

            #return tkn

        return None

    def q5(self):
        self.coluna += 1
        try:
            self.carac_decoded.encode('ascii')
        except UnicodeEncodeError:
            self.sinaliza_erro("[Q5]Não é um caractere ASCII", self.linha, self.coluna_inicial)
            return None
        else:
            self.num_estado = 6
            self.lexema.append(self.carac_decoded)

        return None

    def q6(self):
        self.coluna += 1
        if self.carac_decoded is self.EOF:
            self.num_estado = 0
            self.sinaliza_erro("[Q6]Aspas simples não fechada", self.linha, self.coluna_inicial)
        elif self.carac_decoded is "'":
            self.lexema.append(self.carac_decoded)
            self.num_estado = 0
            #tkn = self.tabela_de_simbolos.retorna_token(''.join(self.lexema))

            #if tkn is None:
            return Token(Tipo.CON_CHAR, ''.join(self.lexema))

            #return tkn
        else:
            carac_para_mensagem = self.carac_decoded
            if self.carac_decoded in ["\r", "\n"]:
                if self.carac_decoded is "\n":
                    self.linha += 1
                    self.coluna = 1
                    carac_para_mensagem = "Quebra de linha"

            self.sinaliza_erro("[Q6]Caractere '{}' é inválido. É esperado uma aspas simples".format(carac_para_mensagem), self.linha, self.coluna - 1)

        return None

    def q8(self):
        self.coluna += 1
        if self.carac_decoded is self.EOF:
            self.sinaliza_erro("[Q8]Literal não fechado até o final do arquivo!".format(self.carac_decoded), self.linha, self.coluna)
            return Token(Tipo.EOF, "EOF")
        elif self.carac_decoded in ["\r", "\n"]:
            if self.carac_decoded is "\n":
                self.linha += 1
                self.coluna = 1
            self.sinaliza_erro("[Q8]Não é permitida a construção de um literal em duas linhas", self.linha, self.coluna_inicial)
        else:
            self.num_estado = 9
            self.lexema.append(self.carac_decoded)

        return None

    def q9(self):
        self.coluna += 1
        if self.carac_decoded in ["\r", "\n"]:
            self.linha += 1
            self.coluna = 1
            self.sinaliza_erro("[Q9]Não é permitida a construção de um literal em duas linhas", self.linha, self.coluna_inicial)
        elif self.carac_decoded is '"':
            self.lexema.append(self.carac_decoded)
            self.num_estado = 0
            #tkn = self.tabela_de_simbolos.retorna_token(''.join(self.lexema))

            #if tkn is None:
            return Token(Tipo.LIT, ''.join(self.lexema))

            #return tkn
        else:
            self.lexema.append(self.carac_decoded)

        return None

    def q11(self):
        self.coluna += 1
        if self.carac_decoded is self.EOF:
            self.sinaliza_erro("[Q11]ID não fechado até o final do arquivo!".format(self.carac_decoded), self.linha, self.coluna)
            return Token(Tipo.EOF, "EOF")
        elif self.carac_decoded.isalpha() or self.carac_decoded.isdigit() or self.carac_decoded is "_":
            self.num_estado = 11
            self.lexema.append(self.carac_decoded)
        elif self.carac_decoded in [" ", "\r", "\n"]:
            self.num_estado = 12
            self.retorna_ponteiro()
            tkn = self.tabela_de_simbolos.retorna_token(''.join(self.lexema))

            if tkn is None:
                return Token(Tipo.ID, ''.join(self.lexema))

            return tkn
        else:
            self.sinaliza_erro("[Q11]Caractere '{}' inválido. É esperado um caractere válido!".format(self.carac_decoded), self.linha, self.coluna)

        return None

    def q19(self):
        self.coluna += 1
        if self.carac_decoded is "=":
            self.num_estado = 0
            return Token(Tipo.OP_EQ, "==")
        else:
            self.retorna_ponteiro()
            return Token(Tipo.OP_ASS, "=")

    def q22(self):
        self.coluna += 1
        if self.carac_decoded is "/":
            self.num_estado = 24
        elif self.carac_decoded is "*":
            self.num_estado = 25
        else:
            self.retorna_ponteiro()
            return Token(Tipo.OP_DIV, "/")

        return None

    def q24(self):
        self.coluna += 1
        if self.carac_decoded is self.EOF:
            self.sinaliza_erro("[Q24]Comentário de uma linha não fechado")
            return Token(Tipo.EOF, "EOF")
        elif self.carac_decoded is "\n":
            self.linha += 1
            self.coluna = 1
            self.num_estado = 0
            print("Comentário de 1 linha descartado>. Linha: {} Coluna: {}".format(self.linha, self.coluna - 1))
        else:
            self.num_estado = 24

        return None

    def q25(self):
        self.coluna += 1
        if self.carac_decoded is self.EOF:
            self.sinaliza_erro("[Q25]Comentário de múltiplas linhas não fechado", self.linha, self.coluna - 1)
            return Token(Tipo.EOF, "EOF")
        elif self.carac_decoded is "*":
            self.num_estado = 26
        else:
            if self.carac_decoded is "\n":
                self.linha += 1
                self.coluna = 1
            self.num_estado = 25

        return None

    def q26(self):
        self.coluna += 1
        if self.carac_decoded is self.EOF:
            self.sinaliza_erro("[Q26]Comentário de múltiplas linhas não fechado", self.linha, self.coluna - 1)
            return Token(Tipo.EOF, "EOF")
        elif self.carac_decoded is "/":
            self.num_estado = 0
            print("Comentário múltiplas linhas descartado. Linha: {} Coluna: {}".format(self.linha, self.coluna - 1))
        elif self.carac_decoded is "*":
            self.num_estado = 26
        else:
            self.num_estado = 25

        return None

    def q31(self):
        self.coluna += 1
        if self.carac_decoded is "=":
            self.num_estado = 0
            return Token(Tipo.OP_LE, "<=")
        else:
            self.retorna_ponteiro()
            return Token(Tipo.OP_LT, "<")

    def q34(self):
        self.coluna += 1
        if self.carac_decoded is "=":
            self.num_estado = 0
            return Token(Tipo.OP_GE, ">=")
        else:
            self.retorna_ponteiro()
            return Token(Tipo.OP_GT, ">")

    def q37(self):
        self.coluna += 1
        if self.carac_decoded is "=":
            self.num_estado = 0
            return Token(Tipo.OP_NE, "!=")
        else:
            carac_para_mensagem = self.carac_decoded
            if self.carac_decoded is "\n":
                self.linha += 1
                self.coluna = 1
                carac_para_mensagem = "Quebra de linha"
            self.sinaliza_erro("[Q37]Caractere {} inválido".format(carac_para_mensagem), self.linha, self.coluna)

        return None

    def proximo_token(self, switch):
        token = None
        self.lexema = []

        while True:
            self.carac = self.arquivo.read(1)
            self.carac_decoded = self.carac.decode("latin1")
            self.carac_decoded = self.carac_decoded.lower() if self.carac_decoded.isalpha() else self.carac_decoded
            estado = switch.get(self.num_estado)

            if estado is not None:
                token = estado() # Executa o estado
                if token is not None:
                    return token

    def retorna_ponteiro(self):
        self.arquivo.seek(-1, 1)
        self.coluna -= 1
        self.num_estado = 0

    def sinaliza_erro(self, mensagem, linha, coluna):
        print("Erro: {}. Linha: {} Coluna: {}".format(mensagem, linha, coluna))

if __name__ == "__main__":
    lexer = Lexer()
    switch = {
        0: lexer.q0,
        1: lexer.q1,
        2: lexer.q2,
        3: lexer.q3,
        5: lexer.q5,
        6: lexer.q6,
        8: lexer.q8,
        9: lexer.q9,
        11: lexer.q11,
        19: lexer.q19,
        22: lexer.q22,
        24: lexer.q24,
        25: lexer.q25,
        26: lexer.q26,
        31: lexer.q31,
        34: lexer.q34,
        37: lexer.q37
    }

    while True:
        token_retornado = lexer.proximo_token(switch)
        token = lexer.tabela_de_simbolos.retorna_token(token_retornado.lexema)

        if token_retornado.classe is Tipo.EOF:
            print(token_retornado.formata_token_print(lexer.linha, lexer.coluna_inicial))
            break

        if token is None:
            lexer.tabela_de_simbolos.add(token_retornado, InfIdentificador())
            #print("Token <{},{}> adicionado à Tabela de Símbolos!".format(token_retornado.classe.name, token_retornado.lexema))
        elif token.classe is Tipo.KW:
            token_retornado.classe = Tipo.KW

        print(token_retornado.formata_token_print(lexer.linha, lexer.coluna_inicial))

    lexer.arquivo.close()
    print("Fim Lexer")
    print("-" * 30)
    #print("> IMPRESSÃO DA TABELA DE SIMBOLOS")
    #lexer.tabela_de_simbolos.imprime_ts()