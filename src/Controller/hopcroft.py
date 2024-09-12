def hopcroft_minimization(afd):
    states = set(afd.keys())
    alphabet = {symbol for trans in afd.values() for symbol in trans.keys() if trans[symbol] is not None}
    
    final_states = {state for state in afd if all(dest is None for dest in afd[state].values())}
    non_final_states = states - final_states
    
    P = [final_states, non_final_states]
    
    W = [final_states, non_final_states]
    
    while W:
        A = W.pop() 
        for c in alphabet:
            X = {state for state in states if afd[state][c] in A}
            
            new_P = []
            for Y in P:
                intersection = X.intersection(Y)
                difference = Y.difference(X)
                if intersection and difference:
                    new_P.append(intersection)
                    new_P.append(difference)
                    if Y in W:
                        W.remove(Y)
                        W.append(intersection)
                        W.append(difference)
                    else:
                        W.append(intersection if len(intersection) <= len(difference) else difference)
                else:
                    new_P.append(Y)
            P = new_P

    minimized_afd = {}
    state_map = {}  
    for partition in P:
        repr_state = next(iter(partition))
        state_map.update({state: repr_state for state in partition})
        minimized_afd[repr_state] = {}

    for state in minimized_afd:
        for symbol in alphabet:
            dest_state = afd[state][symbol]
            minimized_afd[state][symbol] = state_map[dest_state] if dest_state else None

    return minimized_afd