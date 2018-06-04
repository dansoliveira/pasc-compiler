from lexer import Lexer
from parser import Parser

if __name__ == "__main__":
    lexer = Lexer("teste_pasc1.psc")
    parser = Parser(lexer)

    parser.executa()
