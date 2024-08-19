def shunting_yard_regex(expression, verbose=False):
    precedence = {'*': 3, '': 2, '+': 1}
    associative = {'*': 'R', '': 'L', '+': 'L'}
    output = []
    operators = []
    
    if verbose:
        print(f"Processing expression: {expression}")

    i = 0
    while i < len(expression):
        token = expression[i]

        if token.isalnum() or token == '#':
            output.append(token)
            if verbose:
                print(f"Adding {token} to output")
        elif token in precedence:
            while (operators and operators[-1] != '(' and
                   (precedence[operators[-1]] > precedence[token] or
                    (precedence[operators[-1]] == precedence[token] and associative[token] == 'L'))):
                popped = operators.pop()
                output.append(popped)
                if verbose:
                    print(f"Popped {popped} from operators and added to output")
            operators.append(token)
            if verbose:
                print(f"Added {token} to operators")
        elif token == '(':
            operators.append(token)
            if verbose:
                print("Added '(' to operators")
        elif token == ')':
            while operators and operators[-1] != '(':
                popped = operators.pop()
                output.append(popped)
                if verbose:
                    print(f"Popped {popped} from operators and added to output")
            operators.pop()
            if verbose:
                print("Popped '(' from operators")
        
        if i + 1 < len(expression):
            next_token = expression[i + 1]
            if (token.isalnum() or token == ')' or token == '*' or token == '#') and (next_token.isalnum() or next_token == '(' or next_token == '#'):
                if not (token == '*' and next_token == '*'):
                    operators.append('')
                    if verbose:
                        print("Added implicit concatenation operator")
        i += 1

    while operators:
        popped = operators.pop()
        output.append(popped)
        if verbose:
            print(f"Popped {popped} from operators and added to output")

    return ''.join(output)
