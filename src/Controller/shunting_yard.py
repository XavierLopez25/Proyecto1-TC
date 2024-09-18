def handle_operator(token, operators, output, precedence, associative, verbose):
    while operators:
        top_operator = operators[-1]
        if top_operator == '(':
            break
        if (precedence[top_operator] > precedence[token]) or \
           (precedence[top_operator] == precedence[token] and associative[token] == 'L'):
            output.append(operators.pop())
            if verbose:
                print(f"Popped {top_operator} from operators due to precedence and added to output")
        else:
            break
    operators.append(token)
    if verbose:
        print(f"Added {token} to operators")


def shunting_yard_regex(expression, verbose=False):
    precedence = {'*': 3, '+': 3, '?': 3, '|': 1, '': 2}  # Asegurar que la concatenación implícita tiene precedencia definida
    associative = {'*': 'R', '+': 'R', '?': 'R', '|': 'L', '': 'L'}
    output = []
    operators = []
    last_was_operand_or_close = False  # Para manejar la inserción de concatenaciones implícitas

    if verbose:
        print(f"Processing expression: {expression}")

    i = 0
    while i < len(expression):
        token = expression[i]
        if token.isalnum() or token == '#':
            if last_was_operand_or_close:  # Inserción de concatenación implícita si procede
                handle_operator('', operators, output, precedence, associative, verbose)
            output.append(token)
            last_was_operand_or_close = True
        elif token in precedence:
            handle_operator(token, operators, output, precedence, associative, verbose)
            last_was_operand_or_close = token == '*' or token == '+' or token == '?'  # Mantener después de operadores que no requieren otro operando directamente después
        elif token == '(':
            if last_was_operand_or_close:  # Inserción de concatenación implícita antes de '(' si procede
                handle_operator('', operators, output, precedence, associative, verbose)
            operators.append(token)
            last_was_operand_or_close = False
        elif token == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            operators.pop()
            last_was_operand_or_close = True  # ')' se comporta como un operando para la concatenación

        i += 1

    while operators:
        output.append(operators.pop())

    return ''.join(output)
