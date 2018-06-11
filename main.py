from lexer import Lexer
from parser import Parser

if __name__ == "__main__":
    lexer = Lexer("teste2.pasc")
    parser = Parser(lexer)

    parser.executa()

    lexer.tabela_de_simbolos.imprime_ts()