def epsilon_closure(states, nfa):
    print(f"Calculando epsilon-closure para los estados: {states}")
    closure = set(states)
    stack = list(states)
    while stack:
        current = stack.pop()
        print(f"Procesando el estado: {current}")
        
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
    print(f"Clausura epsilon final: {closure}")
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


def normalize_state_name(state):
    """Normaliza el nombre del estado eliminando el asterisco si lo tiene."""
    return state.rstrip('*')

def subset_construction(nfa, start_state):
    initial = epsilon_closure({start_state}, nfa)
    states = [initial]
    dfa = {}
    state_names = {initial: 'S0'}
    state_count = 1
    accepting_states = set()

    # Identificar los estados de aceptación en el NFA, incluyendo versiones con y sin asterisco
    nfa_accepting_states = {state.rstrip('*') for state in nfa if '*' in state}
    nfa_accepting_states.update({state + '*' for state in nfa_accepting_states})  # Añadir versiones con asterisco

    # Verificar si el estado inicial incluye algún estado de aceptación del NFA
    if any(normalize_state_name(state) in nfa_accepting_states for state in initial):
        accepting_states.add('S0')

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

                if any(normalize_state_name(state) in nfa_accepting_states for state in next_closure):
                    accepting_states.add(state_names[next_closure])
            else:
                dfa[current_name][symbol] = None

    # Construir el AFD resultante, marcando los estados de aceptación
    result_dfa = {}
    for state, transitions in dfa.items():
        state_suffix = '*' if state in accepting_states else ''
        result_dfa[state + state_suffix] = {k: v if v in state_names.values() else None for k, v in transitions.items()}

    return result_dfa
