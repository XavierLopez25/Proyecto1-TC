def epsilon_closure(states, nfa):
    """Calcula la clausura epsilon de un conjunto de estados dado."""
    closure = set(states)
    stack = list(states)
    while stack:
        current = stack.pop()
        if 'EPSILON' in nfa[current]:
            for next_state in nfa[current]['EPSILON']:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
    return frozenset(closure)  # Devolver un frozenset para garantizar que sea hashable.

def move(states, symbol, nfa):
    """Encuentra los estados alcanzables desde un conjunto de estados a través de un símbolo."""
    result = set()
    for state in states:
        if symbol in nfa[state]:
            result.update(nfa[state][symbol])
    return frozenset(result)  # Usar frozenset para que el resultado pueda ser usado como clave en diccionarios.

def subset_construction(nfa, start_state):
    """Construye un AFD a partir de un AFN utilizando el método de construcción de subconjuntos."""
    initial = epsilon_closure({start_state}, nfa)  # Asegurarse de pasar un conjunto.
    states = [initial]  # Ya es un frozenset.
    dfa = {}
    state_names = {initial: 'S0'}
    state_count = 1

    while states:
        current = states.pop()
        current_name = state_names[current]
        dfa[current_name] = {}
        alphabet = set(sym for state in nfa for sym in nfa[state] if sym != 'EPSILON')

        for symbol in alphabet:
            next_closure = epsilon_closure(move(current, symbol, nfa), nfa)
            if next_closure:
                if next_closure not in state_names:
                    state_names[next_closure] = f'S{state_count}'
                    states.append(next_closure)
                    state_count += 1
                dfa[current_name][symbol] = state_names[next_closure]
            else:
                dfa[current_name][symbol] = None  # Considerar agregar un estado trampa.

    return dfa
