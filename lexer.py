from lexer_tools import *
import sys

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

    def __init__(self, nome_arquivo):
        try:
            self.arquivo = open(nome_arquivo, "rb")
        except OSError as err:
            print('[ERRO] Não foi possível abrir o arquivo. Motivo: {}'.format(err))
            sys.exit(1)

        self.switch = {
            0: self.q0,
            1: self.q1,
            2: self.q2,
            3: self.q3,
            5: self.q5,
            6: self.q6,
            8: self.q8,
            9: self.q9,
            11: self.q11,
            19: self.q19,
            22: self.q22,
            24: self.q24,
            25: self.q25,
            26: self.q26,
            31: self.q31,
            34: self.q34,
            37: self.q37
        }

    def q0(self):
        if self.carac_decoded is self.EOF:
            return Token(Tipo.EOF, "EOF", self.linha, self.coluna_inicial)
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
            return Token(Tipo.SMB_SEM, ";", self.linha, self.coluna_inicial)
        elif self.carac_decoded is ",":
            self.coluna_inicial = self.coluna
            self.coluna += 1
            return Token(Tipo.SMB_COM, ",", self.linha, self.coluna_inicial)
        elif self.carac_decoded is ")":
            self.coluna_inicial = self.coluna
            self.coluna += 1
            return Token(Tipo.SMB_CPA, ")", self.linha, self.coluna_inicial)
        elif self.carac_decoded is "(":
            self.coluna_inicial = self.coluna
            self.coluna += 1
            return Token(Tipo.SMB_OPA, "(", self.linha, self.coluna_inicial)
        elif self.carac_decoded is "}":
            self.coluna_inicial = self.coluna
            self.coluna += 1
            return Token(Tipo.SMB_CBC, "}", self.linha, self.coluna_inicial)
        elif self.carac_decoded is "{":
            self.coluna_inicial = self.coluna
            self.coluna += 1
            return Token(Tipo.SMB_OBC, "{", self.linha, self.coluna_inicial)
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
            return Token(Tipo.OP_MUL, "*", self.linha, self.coluna_inicial)
        elif self.carac_decoded is "-":
            self.coluna_inicial = self.coluna
            self.coluna += 1
            return Token(Tipo.OP_MIN, "-", self.linha, self.coluna_inicial)
        elif self.carac_decoded is "+":
            self.coluna_inicial = self.coluna
            self.coluna += 1
            return Token(Tipo.OP_AD, "+", self.linha, self.coluna_inicial)
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
        else:
            self.sinaliza_erro("[Q0]Caractere '{}' inválido".format(self.carac_decoded), self.linha, self.coluna_inicial)

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
            return Token(Tipo.CON_NUM, ''.join(self.lexema), self.linha, self.coluna_inicial)

        return None

    def q2(self):
        self.coluna += 1
        if self.carac_decoded.isdigit():
            self.num_estado = 3
            self.lexema.append(self.carac_decoded)
        else:
            self.sinaliza_erro("[Q2]Caractere '{}' inválido. É esperado um dígito.".format(self.carac_decoded), self.linha, self.coluna_inicial)

        return None

    def q3(self):
        self.coluna += 1
        if self.carac_decoded.isdigit():
            self.num_estado = 3
            self.lexema.append(self.carac_decoded)
        else:
            self.retorna_ponteiro()
            return Token(Tipo.CON_NUM, ''.join(self.lexema), self.linha, self.coluna_inicial)

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
            return Token(Tipo.CON_CHAR, ''.join(self.lexema), self.linha, self.coluna_inicial)
        else:
            carac_para_mensagem = self.carac_decoded
            if self.carac_decoded in ["\r", "\n"]:
                if self.carac_decoded is "\n":
                    self.linha += 1
                    self.coluna = 1
                    self.coluna_inicial = 1
                    carac_para_mensagem = "Quebra de linha"

            self.sinaliza_erro("[Q6]Caractere '{}' é inválido. É esperado uma aspas simples".format(carac_para_mensagem), self.linha, self.coluna_inicial)

        return None

    def q8(self):
        self.coluna += 1
        if self.carac_decoded is self.EOF:
            self.sinaliza_erro("[Q8]Literal não fechado até o final do arquivo!", self.linha, self.coluna_inicial)
            return Token(Tipo.EOF, "EOF", self.linha, self.coluna_inicial)
        elif self.carac_decoded in ["\r", "\n"]:
            if self.carac_decoded is "\n":
                self.linha += 1
                self.coluna = 1
                self.coluna_inicial = 1
            self.sinaliza_erro("[Q8]Não é permitida a construção de um literal em duas linhas", self.linha, self.coluna_inicial)
        else:
            self.num_estado = 9
            self.lexema.append(self.carac_decoded)

        return None

    def q9(self):
        self.coluna += 1
        if self.carac_decoded is self.EOF:
            self.sinaliza_erro("[Q9]Literal não fechado até o final do arquivo", self.linha, self.coluna_inicial)
            return Token(Tipo.EOF, "EOF", self.linha, self.coluna_inicial)
        elif self.carac_decoded in ["\r", "\n"]:
            self.linha += 1
            self.coluna = 1
            self.coluna_inicial = 1
            self.sinaliza_erro("[Q9]Não é permitida a construção de um literal em duas linhas", self.linha, self.coluna_inicial)
        elif self.carac_decoded is '"':
            self.lexema.append(self.carac_decoded)
            self.num_estado = 0
            return Token(Tipo.LIT, ''.join(self.lexema), self.linha, self.coluna_inicial)
        else:
            self.lexema.append(self.carac_decoded)

        return None

    def q11(self):
        self.coluna += 1
        if self.carac_decoded is self.EOF:
            self.sinaliza_erro("[Q11]ID não fechado até o final do arquivo", self.linha, self.coluna_inicial)
            return Token(Tipo.EOF, "EOF", self.linha, self.coluna_inicial)
        elif self.carac_decoded.isalpha() or self.carac_decoded.isdigit():
            self.num_estado = 11
            self.lexema.append(self.carac_decoded)
        else:
            self.num_estado = 12
            self.retorna_ponteiro()
            tkn = self.tabela_de_simbolos.retorna_token(''.join(self.lexema))

            if tkn is None:
                return Token(Tipo.ID, ''.join(self.lexema), self.linha, self.coluna_inicial)

            return tkn

        return None

    def q19(self):
        self.coluna += 1
        if self.carac_decoded is "=":
            self.num_estado = 0
            return Token(Tipo.OP_EQ, "==", self.linha, self.coluna_inicial)
        else:
            self.retorna_ponteiro()
            return Token(Tipo.OP_ASS, "=", self.linha, self.coluna_inicial)

    def q22(self):
        self.coluna += 1
        if self.carac_decoded is "/":
            self.num_estado = 24
        elif self.carac_decoded is "*":
            self.num_estado = 25
        else:
            self.retorna_ponteiro()
            return Token(Tipo.OP_DIV, "/", self.linha, self.coluna_inicial)

        return None

    def q24(self):
        self.coluna += 1
        if self.carac_decoded is self.EOF:
            self.sinaliza_erro("[Q24]Comentário de uma linha não fechado", self.linha, self.coluna_inicial)
            return Token(Tipo.EOF, "EOF", self.linha, self.coluna_inicial)
        elif self.carac_decoded is "\n":
            self.linha += 1
            self.coluna = 1
            self.coluna_inicial = 1
            self.num_estado = 0
            #print("Comentário de 1 linha descartado. Linha: {} Coluna: {}".format(self.linha, self.coluna_inicial))
        else:
            self.num_estado = 24

        return None

    def q25(self):
        self.coluna += 1
        if self.carac_decoded is self.EOF:
            self.sinaliza_erro("[Q25]Comentário de múltiplas linhas não fechado", self.linha, self.coluna_inicial)
            return Token(Tipo.EOF, "EOF", self.linha, self.coluna_inicial)
        elif self.carac_decoded is "*":
            self.num_estado = 26
        else:
            if self.carac_decoded is "\n":
                self.linha += 1
                self.coluna = 1
                self.coluna_inicial = 1
            self.num_estado = 25

        return None

    def q26(self):
        self.coluna += 1
        if self.carac_decoded is self.EOF:
            self.sinaliza_erro("[Q26]Comentário de múltiplas linhas não fechado", self.linha, self.coluna_inicial)
            return Token(Tipo.EOF, "EOF", self.linha, self.coluna_inicial)
        elif self.carac_decoded is "/":
            self.num_estado = 0
            #print("Comentário múltiplas linhas descartado. Linha: {} Coluna: {}".format(self.linha, self.coluna_inicial))
        elif self.carac_decoded is "*":
            self.num_estado = 26
        else:
            self.num_estado = 25

        return None

    def q31(self):
        self.coluna += 1
        if self.carac_decoded is "=":
            self.num_estado = 0
            return Token(Tipo.OP_LE, "<=", self.linha, self.coluna_inicial)
        else:
            self.retorna_ponteiro()
            return Token(Tipo.OP_LT, "<", self.linha, self.coluna_inicial)

    def q34(self):
        self.coluna += 1
        if self.carac_decoded is "=":
            self.num_estado = 0
            return Token(Tipo.OP_GE, ">=", self.linha, self.coluna_inicial)
        else:
            self.retorna_ponteiro()
            return Token(Tipo.OP_GT, ">", self.linha, self.coluna_inicial)

    def q37(self):
        self.coluna += 1
        if self.carac_decoded is "=":
            self.num_estado = 0
            return Token(Tipo.OP_NE, "!=", self.linha, self.coluna_inicial)
        else:
            carac_para_mensagem = self.carac_decoded
            if self.carac_decoded is "\n":
                self.linha += 1
                self.coluna = 1
                self.coluna_inicial = 1
                carac_para_mensagem = "Quebra de linha"
            self.sinaliza_erro("[Q37]Caractere {} inválido".format(carac_para_mensagem), self.linha, self.coluna_inicial)

        return None

    def proximo_token(self):
        token_encontrado = None
        self.lexema = []

        while True:
            self.carac = self.arquivo.read(1)
            self.carac_decoded = self.carac.decode("latin1")
            self.carac_decoded = self.carac_decoded.lower() if self.carac_decoded.isalpha() else self.carac_decoded
            estado = self.switch.get(self.num_estado)

            if estado is not None:
                token_encontrado = estado() # Executa o estado
                if token_encontrado is not None:
                    token = self.tabela_de_simbolos.retorna_token(token_encontrado.lexema)
                    if token_encontrado.classe is Tipo.EOF:
                        print(token_encontrado.formata_token_print(self.linha, self.coluna_inicial))
                        self.fechar_arquivo()
                        self.tabela_de_simbolos.imprime_ts()
                        sys.exit(0)

                    if token is None:
                        self.tabela_de_simbolos.add(token_encontrado, InfIdentificador())
                    elif token.classe is Tipo.KW:
                        token_encontrado.classe = Tipo.KW

                    print(token_encontrado.formata_token_print(self.linha, self.coluna_inicial))

                    return token_encontrado

    def fechar_arquivo(self):
        self.arquivo.close()

    def retorna_ponteiro(self):
        self.arquivo.seek(-1, 1)
        self.coluna -= 1
        self.num_estado = 0

    def sinaliza_erro(self, mensagem, linha, coluna):
        print("[LEXER][ERRO]: {}. Linha: {} Coluna: {}".format(mensagem, linha, coluna))
