def remove_acceptance_marks(afd):
    new_afd = {}
    acceptance_states = set()
    
    for state, transitions in afd.items():
        if '*' in state:
            acceptance_states.add(state.replace('*', ''))
            state = state.replace('*', '')
        new_afd[state] = transitions
    
    return new_afd, acceptance_states

def hopcroft_minimization(afd):


    afd, acceptance_states = remove_acceptance_marks(afd)

    states = set(afd.keys())
    alphabet = set(next(iter(afd.values())).keys())  # Asumimos que todos los estados tienen el mismo alfabeto
    non_acceptance_states = states - acceptance_states
    
    # Verificar si el autómata tiene un solo estado y ese estado no tiene transiciones
    if len(afd) == 1 and all(not transitions for transitions in afd.values()):
        # Además, verificar si ese único estado es un estado de aceptación
        only_state = next(iter(afd))
        if only_state in acceptance_states:
            return {only_state + '*': {}}  # Marcamos el estado como de aceptación

    # Inicialización de las particiones

    # Inicialización de particiones considerando los estados de aceptación
    acceptance_partition = {state for state in afd if '*' in state}
    non_acceptance_partition = set(afd.keys()) - acceptance_partition
    partitions = [acceptance_partition, non_acceptance_partition] if acceptance_partition else [non_acceptance_partition]

    def find_partition(state):
        if state is None:
            return None
        for part in partitions:
            if state in part:
                return part
        return None

    # Dividir particiones hasta que no se puedan dividir más
    def refine(partition, symbol):
        new_partitions = {}
        for state in partition:
            next_state = afd[state][symbol] if symbol in afd[state] else None
            # Identificar si el próximo estado es un estado de aceptación
            accepting_transition = '*' in next_state if next_state else False
            # Crear una clave que incluya la información de aceptación
            transition_key = (next_state, accepting_transition)

            if transition_key not in new_partitions:
                new_partitions[transition_key] = set()
            new_partitions[transition_key].add(state)

        return list(new_partitions.values())


    changed = True
    while changed:
        changed = False
        for partition in partitions[:]:
            for symbol in alphabet:
                refined = refine(partition, symbol)
                if len(refined) > 1:
                    partitions.remove(partition)
                    partitions.extend(refined)
                    changed = True
                    break
            if changed:
                break

    # Construir el AFD minimizado
    minimized_afd = {}
    partition_names = {}

    # Generar nombres de particiones y guardar en un diccionario
    for partition in partitions:
        partition_name = '{' + ','.join(sorted(partition)) + '}'
        is_accepting = any(state in acceptance_states for state in partition)
        if is_accepting:
            partition_name += '*'
        partition_names[frozenset(partition)] = partition_name
        minimized_afd[partition_name] = {}

    # Añadir transiciones a cada partición
    for partition in partitions:
        partition_name = partition_names[frozenset(partition)]
        for symbol in alphabet:
            representative_state = next(iter(partition))
            next_state = afd[representative_state][symbol]
            if next_state is None:
                minimized_afd[partition_name][symbol] = None
            else:
                next_partition = find_partition(next_state)
                next_partition_name = partition_names[frozenset(next_partition)]

                # Verificar si es una transición hacia sí mismo
                if partition == next_partition:
                    next_partition_name = partition_name

                minimized_afd[partition_name][symbol] = next_partition_name

                # Si todas las transiciones son hacia sí mismo, asegurar que estén registradas
                if all(afd[state][symbol] == representative_state for state in partition):
                    minimized_afd[partition_name][symbol] = partition_name


    return minimized_afd
