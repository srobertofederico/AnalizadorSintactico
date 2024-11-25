import ply.yacc as yacc
from domain.token import tokens

# Grammar rules
def p_program(p):
    '''
    program : statement_list
    '''
    p[0] = ('program', p[1])

def p_statement_list(p):
    '''
    statement_list : statement
                   | statement_list statement
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''
    statement : assignment END_OF_LINE
              | declaration END_OF_LINE
              | if_statement
    '''
    p[0] = ('statement', p[1])

def p_declaration(p):
    '''
    declaration : VAR NAME
                | VAR NAME ASSIGN expression
    '''
    if len(p) == 3:
        p[0] = ('declare', p[2], None)
    else:
        p[0] =  ('declare', p[2], p[4])

def p_assignment(p):
    '''
    assignment : NAME ASSIGN expression
    '''
    p[0] = ('assign', p[1], p[3])

def p_if_statement(p):
    '''
    if_statement : IF LPAREN condition RPAREN block
                 | IF LPAREN condition RPAREN block ELSE block
    '''
    if len(p) == 6:
        p[0] = ('if', p[3], p[5], None)
    else:
        p[0] = ('if', p[3], p[5], p[7])

def p_condition(p):
    '''
    condition : expression EQUALS expression
              | expression NOTEQUALS expression
              | expression LESSTHAN expression
              | expression GREATERTHAN expression
              | expression LESSEQUAL expression
              | expression GREATEREQUAL expression
    '''
    p[0] = ('condition', p[2], p[1], p[3])

def p_block(p):
    '''
    block : LBRACE statement_list RBRACE
    '''
    p[0] = ('block', p[2])

def p_expression(p):
    '''
    expression : expression PLUS term
               | expression MINUS term
    '''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_term(p):
    '''
    expression : term
    '''
    p[0] = p[1]

def p_term(p):
    '''
    term : term TIMES factor
         | term DIVIDE factor
    '''
    p[0] = ('binop', p[2], p[1], p[3])

def p_term_factor(p):
    '''
    term : factor
    '''
    p[0] = p[1]

def p_factor(p):
    '''
    factor : NUMBER
           | NAME
           | LPAREN expression RPAREN
    '''
    if len(p) == 2:
        if isinstance(p[1], int):
            p[0] = ('number', p[1])
        else:
            p[0] = ('name', p[1])
    else:
        p[0] = ('grouped', p[2])

def p_error(p):
    if p:
        error_message = f"ERROR: Token inesperado '{p.value}' en la línea {p.lineno}, posición {p.lexpos}."
        suggestion = f"Sugerencia: revise la estructura cerca de '{p.value}'."
        print(error_message)
        raise SyntaxError(f"{error_message}\n{suggestion}")
    else:
        error_message = "ERROR: Fin de archivo inesperado. Posiblemente falta cerrar un bloque o una expresión."
        print(error_message)
        raise SyntaxError(error_message)

# Build the parser
parser = yacc.yacc(errorlog=yacc.NullLogger())  # Anula el log estándar y delega en p_error