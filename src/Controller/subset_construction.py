def epsilon_closure(states, nfa):
    """Calcula la clausura epsilon de un conjunto de estados dado."""
    closure = set(states)
    stack = list(states)
    while stack:
        current = stack.pop()

        # Manejo de estados con asterisco
        if current not in nfa and current + '*' in nfa:
            current = current + '*'  # Usar el estado con asterisco si no se encuentra sin él

        if current not in nfa:
            raise KeyError(f"Estado '{current}' no encontrado en el NFA")

        if 'EPSILON' in nfa[current]:
            for next_state in nfa[current]['EPSILON']:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
    return frozenset(closure)


def move(states, symbol, nfa):
    """Encuentra los estados alcanzables desde un conjunto de estados a través de un símbolo."""
    result = set()
    for state in states:
        # Manejo de estados con asterisco
        if state not in nfa and state + '*' in nfa:
            state = state + '*'  # Usar el estado con asterisco si no se encuentra sin él

        if state not in nfa:
            raise KeyError(f"Estado '{state}' no encontrado en el NFA")

        if symbol in nfa[state]:
            result.update(nfa[state][symbol])
    return frozenset(result)


def subset_construction(nfa, start_state):
    """Construye un AFD a partir de un AFN utilizando el método de construcción de subconjuntos."""
    initial = epsilon_closure({start_state}, nfa)
    states = [initial]
    dfa = {}
    state_names = {initial: 'S0'}
    state_count = 1
    accepting_states = set()

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
                dfa[current_name][symbol] = None

    # Marcar los estados de aceptación en el AFD según las transiciones
    result_dfa = {}
    for state, transitions in dfa.items():
        # Verificar si todas las transiciones son None o apuntan al mismo estado
        is_accepting = all(target is None or target == state for target in transitions.values())
        if is_accepting:
            result_dfa[state + '*'] = transitions  # Marcar estado de aceptación con asterisco
        else:
            result_dfa[state] = transitions

    return result_dfa
