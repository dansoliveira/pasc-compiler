from lexer_tools import *

class Lexer():
    linha = 1
    coluna = 1
    carac = ''
    carac_decoded = ''
    num_estado = 0
    lexema = []
    tabela_de_simbolos = {}
    arquivo = open("/home/daniel/teste_pasc", "rb")

    def q0(self):
        self.carac_decoded = self.carac.decode('utf-8')
        print("q0 " + self.carac_decoded)
        if self.carac_decoded is "":
            return Token(Tipo.EOF, "EOF", self.linha, self.coluna)
        elif self.carac_decoded is "\n":
                self.linha += 1
        elif self.carac_decoded is " ":
                self.coluna += 1
        elif self.carac_decoded is "\t":
                self.coluna += 3
        elif self.carac_decoded.isdigit():
            self.num_estado = 1
            self.lexema.append(self.carac_decoded)

        return None

    def q1(self):
        self.carac_decoded = self.carac.decode('utf-8')
        print("q1 " + self.carac_decoded)
        if self.carac_decoded.isdigit():
            self.num_estado = 1
            self.lexema.append(self.carac_decoded)
        elif self.carac_decoded is ".":
            self.num_estado = 2
            self.lexema.append(self.carac_decoded)
        else:
            print("q4 " + self.carac_decoded)
            self.retorna_ponteiro()
            return Token(Tipo.CON_NUM, ''.join(self.lexema), self.linha, self.coluna)

        return None

    def q2(self):
        self.carac_decoded = self.carac.decode('utf-8')
        print("q2 " + self.carac_decoded)
        if self.carac_decoded.isdigit():
            self.num_estado = 3
            self.lexema.append(self.carac_decoded)

        return None

    def q3(self):
        self.carac_decoded = self.carac.decode('utf-8')
        print("q3 " + self.carac_decoded)
        if self.carac_decoded.isdigit():
            self.num_estado = 3
            self.lexema.append(self.carac_decoded)
        else:
            print("q4 " + self.carac_decoded)
            self.retorna_ponteiro()
            return Token(Tipo.CON_NUM, ''.join(self.lexema), self.linha, self.coluna)

        return None

    def q4(self):
        return ""

    def q5(self):
        return ""

    def q6(self):
        return ""

    def q7(self):
        return ""

    def q8(self):
        return ""

    def q9(self):
        return ""

    def q10(self):
        return ""

    def q11(self):
        return ""

    def q12(self):
        return ""

    def q13(self):
        return ""

    def q14(self):
        return ""

    def q15(self):
        return ""

    def q16(self):
        return ""

    def q17(self):
        return ""

    def q18(self):
        return ""

    def q19(self):
        return ""

    def q20(self):
        return ""

    def q21(self):
        return ""

    def q22(self):
        return ""

    def q23(self):
        return ""

    def q24(self):
        return ""

    def q25(self):
        return ""

    def q26(self):
        return ""

    def q27(self):
        return ""

    def q28(self):
        return ""

    def q29(self):
        return ""

    def q30(self):
        return ""

    def q31(self):
        return ""

    def q32(self):
        return ""

    def q33(self):
        return ""

    def q34(self):
        return ""

    def q35(self):
        return ""

    def q36(self):
        return ""

    def q37(self):
        return ""

    def q38(self):
        return ""

    def proximo_token(self, switch):
        token = None
        self.lexema = []

        while True:
            self.carac = self.arquivo.read(1)
            estado = switch.get(self.num_estado, "Estado não encontrado")
            token = estado()

            if token is not None:  # Executa o estado
                return token

    def retorna_ponteiro(self):
        self.arquivo.seek(-1, 1)
        self.num_estado = 0
        return None


if __name__ == "__main__":
    lexer = Lexer()
    switch = {
        0: lexer.q0,
        1: lexer.q1,
        2: lexer.q2,
        3: lexer.q3,
        4: lexer.q4,
        5: lexer.q5,
        6: lexer.q6,
        7: lexer.q7,
        8: lexer.q8,
        9: lexer.q9,
        10: lexer.q10,
        11: lexer.q11,
        12: lexer.q12,
        13: lexer.q13,
        14: lexer.q14,
        15: lexer.q15,
        16: lexer.q16,
        17: lexer.q17,
        18: lexer.q18,
        19: lexer.q19,
        20: lexer.q20,
        21: lexer.q21,
        22: lexer.q22,
        23: lexer.q23,
        24: lexer.q24,
        25: lexer.q25,
        26: lexer.q26,
        27: lexer.q27,
        28: lexer.q28,
        29: lexer.q29,
        30: lexer.q30,
        31: lexer.q31,
        32: lexer.q32,
        33: lexer.q33,
        34: lexer.q34,
        35: lexer.q35,
        36: lexer.q36,
        37: lexer.q37,
        38: lexer.q38
    }

    while True:
        token = lexer.proximo_token(switch)

        print(token.formata_token_print())

        if token.classe is Tipo.EOF:
            break

    lexer.arquivo.close()
    print("Fim Lexer")

