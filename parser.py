from lexer_tools import Tipo, Token
import sys

class Parser():
    tabela_preditiva = {
        'prog': {'program': 'program id body',
                 Tipo.EOF: 'synch'},
        'body': {'{': 'decl-list { stmt-list }',
                 'num': 'decl-list { stmt-list }',
                 'char': 'decl-list { stmt-list }',
                 Tipo.EOF: None},
        'decl-list': {'{': None,
                      'num': 'decl ; decl-list',
                      'char': 'decl ; decl-list'},
        'decl': {';': 'synch',
                 'num': 'type id-list',
                 'char': 'type id-list'},
        'type': {Tipo.ID: 'synch',
                 'num': 'num',
                 'char': 'char'},
        'id-list': {Tipo.ID: 'id id-list\'',
                    ';': 'synch'},
        'id-list\'': {';': None,
                      ',': ', id-list'},
        'stmt-list': {Tipo.ID: 'stmt ; stmt-list',
                      '}': None,
                      'if': 'stmt ; stmt-list',
                      'while': 'stmt ; stmt-list',
                      'read': 'stmt ; stmt-list',
                      'write': 'stmt ; stmt-list'},
        'stmt': {Tipo.ID: 'assign-stmt',
                 ';': 'synch',
                 'if': 'if-stmt',
                 'while': 'while-stmt',
                 'read': 'read-stmt',
                 'write': 'write-stmt'},
        'assign-stmt': {Tipo.ID: 'id = simple-expr',
                        ';': 'synch'},
        'if-stmt': {';': 'synch',
                    'if': 'if ( condition ) { stmt-list } if-stmt\''},
        'if-stmt\'': {';': None,
                      'else': 'else { stmt-list }'},
        'condition': {Tipo.ID: 'expression',
                      '(': 'expression',
                      ')': 'synch',
                      'not': 'expression',
                      Tipo.CON_NUM: 'expression',
                      Tipo.CON_CHAR: 'expression'},
        'while-stmt': {';': 'synch',
                       'while': 'stmt-prefix { stmt-list }'},
        'stmt-prefix': {'{': 'synch',
                        'while': 'while ( condition )'},
        'read-stmt': {';': 'synch',
                      'read': 'read id'},
        'write-stmt': {';': 'synch',
                       'write': 'write writable'},
        'writable': {Tipo.ID: 'simple-expr',
                     ';': 'synch',
                     '(': 'simple-expr',
                     Tipo.LIT: 'literal',
                     'not': 'simple-expr',
                     Tipo.CON_NUM: 'simple-expr',
                     Tipo.CON_CHAR: 'simple-expr'},
        'expression': {Tipo.ID: 'simple-expr expression\'',
                       '(': 'simple-expr expression\'',
                       ')': 'synch',
                       'not': 'simple-expr expression\'',
                       Tipo.CON_NUM: 'simple-expr expression\'',
                       Tipo.CON_CHAR: 'simple-expr expression\''},
        'expression\'': {')': None,
                         '==': 'relop simple-expr',
                         '>': 'relop simple-expr',
                         '>=': 'relop simple-expr',
                         '<': 'relop simple-expr',
                         '<=': 'relop simple-expr',
                         '!=': 'relop simple-expr'},
        'simple-expr': {Tipo.ID: 'term simple-expr\'',
                        ';': 'synch',
                        '(': 'term simple-expr\'',
                        ')': 'synch',
                        'not': 'term simple-expr\'',
                        '==': 'synch',
                        '>': 'synch',
                        '>=': 'synch',
                        '<': 'synch',
                        '<=': 'synch',
                        '!=': 'synch',
                        Tipo.CON_NUM: 'term simple-expr\'',
                        Tipo.CON_CHAR: 'term simple-expr\''},
        'simple-expr\'': {';': None,
                          ')': None,
                          '==': None,
                          '>': None,
                          '>=': None,
                          '<': None,
                          '<=': None,
                          '!=': None,
                          '+': 'addop term simple-expr\'',
                          '-': 'addop term simple-expr\'',
                          'or': 'addop term simple-expr\''},
        'term': {Tipo.ID: 'factor-a term\'',
                 ';': 'synch',
                 '(': 'factor-a term\'',
                 ')': 'synch',
                 'not': 'factor-a term\'',
                 '==': 'synch',
                 '>': 'synch',
                 '>=': 'synch',
                 '<': 'synch',
                 '<=': 'synch',
                 '!=': 'synch',
                 '+': 'synch',
                 '-': 'synch',
                 'or': 'synch',
                 Tipo.CON_NUM: 'factor-a term\'',
                 Tipo.CON_CHAR: 'factor-a term\''},
        'term\'': {';': None,
                   ')': None,
                   '==': None,
                   '>': None,
                   '>=': None,
                   '<': None,
                   '<=': None,
                   '!=': None,
                   '+': None,
                   '-': None,
                   'or': None,
                   '*': 'mulop factor-a term\'',
                   '/': 'mulop factor-a term\'',
                   'and': 'mulop factor-a term\''},
        'factor-a': {Tipo.ID: 'factor',
                     ';': 'synch',
                     '(': 'factor',
                     'not': 'not factor',
                     '==': 'synch',
                     '>': 'synch',
                     '>=': 'synch',
                     '<': 'synch',
                     '<=': 'synch',
                     '!=': 'synch',
                     '+': 'synch',
                     '-': 'synch',
                     'or': 'synch',
                     '*': 'synch',
                     '/': 'synch',
                     'and': 'synch',
                     Tipo.CON_NUM: 'factor',
                     Tipo.CON_CHAR: 'factor'},
        'factor': {Tipo.ID: 'id',
                   ';': 'synch',
                   '(': '( expression )',
                   ')': 'synch',
                   '==': 'synch',
                   '>': 'synch',
                   '>=': 'synch',
                   '<': 'synch',
                   '<=': 'synch',
                   '!=': 'synch',
                   '+': 'synch',
                   '-': 'synch',
                   'or': 'synch',
                   '*': 'synch',
                   '/': 'synch',
                   'and': 'synch',
                   Tipo.CON_NUM: 'constant',
                   Tipo.CON_CHAR: 'constant'},
        'relop': {Tipo.ID: 'synch',
                  '(': 'synch',
                  'not': 'synch',
                  '==': '==',
                  '>': '>',
                  '>=': '>=',
                  '<': '<',
                  '<=': '<=',
                  '!=': '!=',
                  Tipo.CON_NUM: 'synch',
                  Tipo.CON_CHAR: 'synch'},
        'addop': {Tipo.ID: 'synch',
                  '(': 'synch',
                  'not': 'synch',
                  '+': '+',
                  '-': '-',
                  'or': 'or',
                  Tipo.CON_NUM: 'synch',
                  Tipo.CON_CHAR: 'synch'},
        'mulop': {Tipo.ID: 'synch',
                  '(': 'synch',
                  'not': 'synch',
                  '*': '*',
                  '/': '/',
                  'and': 'and',
                  Tipo.CON_NUM: 'synch',
                  Tipo.CON_CHAR: 'synch'},
        'constant': {';': 'synch',
                     ')': 'synch',
                     '==': 'synch',
                     '>': 'synch',
                     '>=': 'synch',
                     '<': 'synch',
                     '<=': 'synch',
                     '!=': 'synch',
                     '+': 'synch',
                     '-': 'synch',
                     'or': 'synch',
                     '*': 'synch',
                     '/': 'synch',
                     'and': 'synch',
                     Tipo.CON_NUM: 'num_const',
                     Tipo.CON_CHAR: 'char_const'}
    }

    tabela_conversao = {
        'id': Tipo.ID,
        'literal': Tipo.LIT,
        'num_const': Tipo.CON_NUM,
        'char_const': Tipo.CON_CHAR
    }

    def __init__(self, lexer):
        self.lexer = lexer
        self.token_esperado = ''
        self.token_retornado = ''
        self.linha_token_retornado = 0
        self.coluna_token_retornado = 0
        self.qtd_erros = 0
        self.pilha = []
        self.pilha.append('$')
        self.pilha.append('prog')
        self.advance()

    def advance(self):
        token = self.lexer.proximo_token()
        self.linha_token_retornado = token.linha
        self.coluna_token_retornado = token.coluna

        if token.classe in [Tipo.ID, Tipo.LIT, Tipo.CON_NUM, Tipo.CON_CHAR]:
            self.token_retornado = token.classe
        else:
            self.token_retornado = token.lexema

    def synch(self):
        self.sinaliza_erro()
        self.pilha.pop()

    def skip(self):
        self.sinaliza_erro()
        self.advance()

    def formata_token(self, token):
        if isinstance(token, Tipo):
            return str(token).replace('Tipo.', '')
        return token

    def get_tokens_esperados_do_nao_terminal(self, nao_terminal):
        return '\', \''.join(map(self.formata_token, self.tabela_preditiva[nao_terminal].keys()))

    def trata_item_regra(self, item):
        try:
            return self.tabela_conversao[item]
        except KeyError:
            return item

    def is_pilha_vazia(self):
        if len(self.pilha) == 1 and self.pilha[0] == '$':
            return True

        return False

    def executa(self):
        while not self.is_pilha_vazia():
            # Pega o topo da pilha
            x = self.pilha[len(self.pilha) - 1]
            # Se x é um terminal, ou seja, não está nas chaves da TP
            if x not in self.tabela_preditiva.keys():
                if x == self.token_retornado:
                    self.pilha.pop()
                    self.advance()
                else:
                    self.token_esperado = x
                    self.skip()
            else:
                try:
                    if self.tabela_preditiva[x][self.token_retornado] == 'synch':
                        self.token_esperado = self.get_tokens_esperados_do_nao_terminal(x)
                        self.synch()
                    else:
                        self.pilha.pop()
                        regra = self.tabela_preditiva[x][self.token_retornado]
                        if regra:
                            regra_split = regra.split()
                            # loop para empilhar a regra ao contrário
                            for item in list(reversed(regra_split)):
                                self.pilha.append(self.trata_item_regra(item))
                except KeyError:
                    self.token_esperado = self.get_tokens_esperados_do_nao_terminal(x)
                    self.skip()

    def sinaliza_erro(self):
        print("[PARSER][ERRO] O token '{}' na linha '{}', coluna '{}' é inválido. Esperava-se o(s) token(s): '{}'.".format(self.formata_token(self.token_retornado), self.linha_token_retornado, self.coluna_token_retornado, self.token_esperado))
        self.qtd_erros += 1
        if self.qtd_erros is 5:
            print("[FIM_EXECUÇÃO_PARSER] Limite de erros excedido. Qtd. Erros: {}".format(self.qtd_erros))
            sys.exit(1)
