def epsilon_closure(states, nfa, verbose=False):
    if verbose:
        print(f"Calculating epsilon-closure for states: {states}")
    closure = set(states)
    stack = list(states)
    while stack:
        current = stack.pop()
        if verbose:
            print(f"Processing state: {current}")

        # Handle states with an asterisk
        if current not in nfa and current + '*' in nfa:
            current = current + '*'

        if current not in nfa:
            raise KeyError(f"State '{current}' not found in the NFA")

        if 'EPSILON' in nfa[current]:
            for next_state in nfa[current]['EPSILON']:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
    if verbose:
        print(f"Final epsilon-closure: {closure}")
    return frozenset(closure)

def move(states, symbol, nfa, verbose=False):
    if verbose:
        print(f"Moving from states {states} using symbol '{symbol}'")
    result = set()
    for state in states:
        if verbose:
            print(f"Checking state: {state}")
        
        # Handle states with an asterisk if the exact state isn't found
        if state not in nfa and state + '*' in nfa:
            if verbose:
                print(f"State '{state}' not found, using '{state + '*'}'")
            state = state + '*'

        if state not in nfa:
            raise KeyError(f"State '{state}' not found in the NFA")

        # Check if there is a transition for the given symbol
        if symbol in nfa[state]:
            result.update(nfa[state][symbol])
            if verbose:
                print(f"States reachable from {state} on symbol '{symbol}': {nfa[state][symbol]}")
        else:
            if verbose:
                print(f"No transition from {state} on symbol '{symbol}'")

    if verbose:
        print(f"Resulting set of states: {result}")
    return frozenset(result)

def normalize_state_name(state, verbose=False):
    """
    Normalizes the state name by removing the asterisk if it has one.
    """
    normalized_state = state.rstrip('*')
    if verbose:
        print(f"Normalizing state name: {state} -> {normalized_state}")
    return normalized_state

def subset_construction(nfa, start_state, verbose=False):
    initial = epsilon_closure({start_state}, nfa)
    states = [initial]
    dfa = {}
    state_names = {initial: 'S0'}
    state_count = 1
    accepting_states = set()

    if verbose:
        print(f"Starting subset construction with initial state: {initial}")


    # Identify accepting states in the NFA, including versions with and without asterisks
    nfa_accepting_states = {state.rstrip('*') for state in nfa if '*' in state}
    nfa_accepting_states.update({state + '*' for state in nfa_accepting_states})  

    # Check if the initial state includes any accepting states from the NFA
    if any(normalize_state_name(state) in nfa_accepting_states for state in initial):
        accepting_states.add('S0')
        if verbose:
            print(f"Initial state {initial} includes accepting states")

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
                if verbose:
                    print(f"Transition from {current_name} on symbol '{symbol}' to {state_names[next_closure]}")

                if any(normalize_state_name(state) in nfa_accepting_states for state in next_closure):
                    accepting_states.add(state_names[next_closure])
            else:
                dfa[current_name][symbol] = None
                if verbose:
                    print(f"No transitions found from {current_name} on symbol '{symbol}'")


    # Build the resulting DFA, marking accepting states
    result_dfa = {}
    for state, transitions in dfa.items():
        state_suffix = '*' if state in accepting_states else ''
        result_dfa[state + state_suffix] = {k: v if v in state_names.values() else None for k, v in transitions.items()}
        if verbose:
            print(f"State {state} transitions: {transitions}")

    return result_dfa
