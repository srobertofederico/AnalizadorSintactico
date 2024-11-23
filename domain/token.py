import ply.lex as lex

# Tokens
tokens = (
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'NAME', 'NUMBER', 'ASSIGN',
    'IF', 'ELSE',
    'EQUALS', 'NOTEQUALS', 'LESSTHAN', 'GREATERTHAN',
    'LESSEQUAL', 'GREATEREQUAL', 'VAR', 'END_OF_LINE', 'ERROR',
)

# Token definitions
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_ASSIGN = r'='
t_EQUALS = r'=='
t_NOTEQUALS = r'!='
t_LESSTHAN = r'<'
t_GREATERTHAN = r'>'
t_LESSEQUAL = r'<='
t_GREATEREQUAL = r'>='
t_END_OF_LINE = r';'

# Reserved words
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'var': 'VAR',
}

# Name token
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'NAME')  # Check for reserved words
    return t

# Number token
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Newlines
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignored characters
t_ignore = ' \t'

# Error handler for illegal characters
def t_error(t):
    error_mesage = f"ERROR: Error léxico:\nCaracter no válido: {t.value[0]!r} en línea {t.lineno}, posición {t.lexpos}"
    print(error_mesage)
    t.lexer.skip(1)
    t.type = 'ERROR'
    return error_mesage
    
lexer = lex.lex()