import re

# Definición de tokens utilizando expresiones regulares
tokens = [
    ('NUMERO', r'\d+'),
    ('SUMA', r'\+'),
    ('RESTA', r'\-'),
    ('MULTIPLICACION', r'\*'),
    ('DIVISION', r'\/'),
    ('ESPACIO', r'\s+'),
]

# Función para realizar el análisis léxico
def lexer(expr):
    # Lista de tokens encontrados
    token_list = []
    # Recorre la expresión en busca de tokens
    while expr:
        for token_name, pattern in tokens:
            match = re.match(pattern, expr)
            if match:
                value = match.group(0)
                if token_name != 'ESPACIO':  # Ignorar los espacios
                    token_list.append((token_name, value))
                expr = expr[len(value):]
                break
        else:
            raise ValueError("No se pudo analizar la expresión")
    return token_list

# Función para realizar el análisis sintáctico
def parser(tokens):
    # Convierte la lista de tokens en un iterador
    tokens = iter(tokens)
    # Función auxiliar para obtener el próximo token
    def get_next_token():
        return next(tokens, None)

    # Función auxiliar para manejar errores de sintaxis
    def error():
        raise SyntaxError("Error de sintaxis")

    # Reglas de producción
    def factor():
        token = get_next_token()
        if token and token[0] == 'NUMERO':
            return int(token[1])
        elif token and token[0] == 'SUMA':
            return factor()
        elif token and token[0] == 'RESTA':
            return -factor()
        else:
            error()

    def term():
        result = factor()
        while True:
            token = get_next_token()
            if token and token[0] == 'MULTIPLICACION':
                result *= factor()
            elif token and token[0] == 'DIVISION':
                result /= factor()
            else:
                # Devolver el token no consumido
                if token is not None:
                    tokens = iter([token] + list(tokens))
                break
        return result

    def expr():
        result = term()
        while True:
            token = get_next_token()
            if token and token[0] == 'SUMA':
                result += term()
            elif token and token[0] == 'RESTA':
                result -= term()
            else:
                if token is not None:
                    tokens = iter([token] + list(tokens))
                break
        return result

    result = expr()
    token = get_next_token()
    if token:
        error()
    return result

# Función principal
def main():
    expresion = input("Ingrese una expresión matemática: ")
    # Análisis léxico
    token_list = lexer(expresion)
    print("Tokens:", token_list)
    # Análisis sintáctico
    resultado = parser(token_list)
    print("Resultado:", resultado)

if __name__ == "__main__":
    main()
