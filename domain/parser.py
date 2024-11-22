import ply.yacc as yacc
from domain.token import tokens

# Keeping existing rules and adding new ones

def p_statement(p):
    '''
    statement : assignment
              | declaration
              | if_statement
              | expression
    '''
    p[0] = ('statement', p[1])

def p_statement_list(p):
    '''
    statement_list : statement
                  | statement_list statement
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_declaration(p):
    '''
    declaration : VAR NAME
                | VAR NAME ASSIGN expression
    '''
    if len(p) == 3:
        p[0] = ('declare', p[2], None)
    else:
        p[0] = ('declare', p[2], p[4])

def p_assignment(p):
    '''
    assignment : NAME ASSIGN expression
    '''
    p[0] = ('assign', p[1], p[3])

def p_if_statement(p):
    '''
    if_statement : IF condition block
                | IF condition block ELSE block
    '''
    if len(p) == 4:
        p[0] = ('if', p[2], p[3], None)
    else:
        p[0] = ('if', p[2], p[3], p[5])

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
    expression : term PLUS term
               | term MINUS term
    '''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_term(p):
    '''
    expression : term
    '''
    p[0] = p[1]

def p_term(p):
    '''
    term : factor TIMES factor
         | factor DIVIDE factor
    '''
    p[0] = ('binop', p[2], p[1], p[3])

def p_term_factor(p):
    '''
    term : factor
    '''
    p[0] = p[1]

def p_factor_number(p):
    '''
    factor : NUMBER
    '''
    p[0] = ('number', p[1])

def p_factor_name(p):
    '''
    factor : NAME
    '''
    p[0] = ('name', p[1])

def p_factor_unary(p):
    '''
    factor : PLUS factor
           | MINUS factor
    '''
    p[0] = ('unary', p[1], p[2])

def p_factor_grouped(p):
    '''
    factor : LPAREN expression RPAREN
    '''
    p[0] = ('grouped', p[2])

def p_error(p):
    print(f'Syntax error at {p.value!r}')

# Build the parser
parser = yacc.yacc()