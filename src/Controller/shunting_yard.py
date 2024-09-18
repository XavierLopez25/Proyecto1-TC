def shunting_yard_regex(expression, verbose=False):
    # Definir la precedencia y la asociatividad de los operadores
    precedence = {'*': 3, '+': 3, '?': 3, '': 2, '|': 1}
    associative = {'*': 'R', '+': 'R', '?': 'R', '': 'L', '|': 'L'}
    output = []  # Lista de salida para almacenar la notación postfija
    operators = []  # Pila para operadores
    
    if verbose:
        print(f"Processing expression: {expression}")

    i = 0
    while i < len(expression):
        token = expression[i]

        if token.isalnum() or token == '#':
            # Si el token es un carácter alfanumérico (letra o número) o el caracter especial '#'
            output.append(token)
            if verbose:
                print(f"Adding {token} to output")
        elif token in precedence:
            # Si el token es un operador
            while (operators and operators[-1] != '(' and
                   (precedence[operators[-1]] > precedence[token] or
                    (precedence[operators[-1]] == precedence[token] and associative[token] == 'L'))):
                # Desapilar operadores de mayor o igual precedencia
                popped = operators.pop()
                output.append(popped)
                if verbose:
                    print(f"Popped {popped} from operators and added to output")
            operators.append(token)
            if verbose:
                print(f"Added {token} to operators")
        elif token == '(':
            # Si es un paréntesis de apertura
            operators.append(token)
            if verbose:
                print("Added '(' to operators")
        elif token == ')':
            # Si es un paréntesis de cierre, desapilar hasta encontrar '('
            while operators and operators[-1] != '(':
                popped = operators.pop()
                output.append(popped)
                if verbose:
                    print(f"Popped {popped} from operators and added to output")
            operators.pop()  # Quitar el '('
            if verbose:
                print("Popped '(' from operators")

        # Añadir operador de concatenación implícita
        if i + 1 < len(expression):
            next_token = expression[i + 1]
            # Añadir concatenación implícita si el token actual es un símbolo válido para concatenar
            if (token.isalnum() or token == ')' or token in '*+?#') and (next_token.isalnum() or next_token == '(' or next_token == '#'):
                operators.append('')
                if verbose:
                    print("Added implicit concatenation operator")
        
        i += 1

    # Desapilar los operadores restantes
    while operators:
        popped = operators.pop()
        output.append(popped)
        if verbose:
            print(f"Popped {popped} from operators and added to output")

    return ''.join(output)  # Convertir la lista de salida en una cadena

