def shunting_yard_regex(expression):
    precedence = {'*': 3, '': 2, '+': 1}
    associative = {'*': 'R', '+': 'L', '.': 'L'}
    output = []
    operators = []
    
    i = 0
    while i < len(expression):
        token = expression[i]

        if token.isalnum():
            output.append(token)
        elif token in precedence:
            while (operators and operators[-1] != '(' and
                   (precedence[operators[-1]] > precedence[token] or
                    (precedence[operators[-1]] == precedence[token] and associative[token] == 'L'))):
                output.append(operators.pop())
            operators.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            operators.pop()
        
        if i + 1 < len(expression):
            next_token = expression[i + 1]
            if (token.isalnum() or token == ')' or token == '*') and (next_token.isalnum() or next_token == '('):
                operators.append('')

        i += 1

    while operators:
        output.append(operators.pop())
    
    return ''.join(output)
