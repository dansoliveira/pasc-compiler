from lexer import Lexer
from parser import Parser

if __name__ == "__main__":
    lexer = Lexer("exemplos/teste2.pasc")
    parser = Parser(lexer)

    parser.executa()