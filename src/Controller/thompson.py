from Model.node import Node

def regex_to_nfa_thompson(postfix, verbose=False):
    def thompson_construction_postfix(postfix):
        stack = []

        if verbose:
            print(f"Processing postfix: {postfix}")

        for token in postfix:
            if token.isalnum() or token == '#':
                # Si es un carácter alfanumérico o '#', creamos un nodo CHAR
                node = Node('CHAR', value=token)
                stack.append(node)
                if verbose:
                    print(f"Pushed CHAR node for {token} to stack")
            elif token == '*':
                # Si es un operador de Kleene, lo aplicamos al último nodo
                node = stack.pop()
                new_node = Node('KLEENE', [node])
                stack.append(new_node)
                if verbose:
                    print(f"Applied Kleene star to node and pushed to stack")
            elif token == '+':
                # Si es un operador de Plus, lo aplicamos al último nodo
                node = stack.pop()
                new_node = Node('PLUS', [node])
                stack.append(new_node)
                if verbose:
                    print(f"Applied Plus operator to node and pushed to stack")
            elif token == '?':
                # Si es un operador Opcional, lo aplicamos al último nodo
                node = stack.pop()
                new_node = Node('OPTIONAL', [node])
                stack.append(new_node)
                if verbose:
                    print(f"Applied Optional operator to node and pushed to stack")
            elif token == '|':
                # Si es una alternancia (OR), tomamos dos nodos de la pila y creamos uno nuevo
                right = stack.pop()
                left = stack.pop()
                new_node = Node('ALTERNATE', [left, right])
                stack.append(new_node)
                if verbose:
                    print(f"Applied Alternation (OR) between nodes and pushed to stack")
            elif token == '':
                # Concatenación implícita
                right = stack.pop()
                left = stack.pop()
                new_node = Node('CONCAT', [left, right])
                stack.append(new_node)
                if verbose:
                    print(f"Applied Concatenation between nodes and pushed to stack")
            else:
                raise ValueError(f"Unexpected token in postfix: {token}")

        # El último nodo en la pila será el AFN completo
        return stack.pop()

    def thompson_construction(node):
        if verbose:
            print(f"Constructing NFA for node: {node}")

        if node.type == 'CHAR':
            start = {}
            end = {}
            if node.value == '#':
                start['EPSILON'] = [end]
            else:
                start[node.value] = [end]
            if verbose:
                print(f"Created NFA for character {node.value}")
            return start, end

        elif node.type == 'CONCAT':
            current_start, current_end = thompson_construction(node.children[0])
            for child in node.children[1:]:
                next_start, next_end = thompson_construction(child)
                current_end['EPSILON'] = [next_start]
                current_end = next_end
            return current_start, current_end

        elif node.type == 'ALTERNATE':
            start = {}
            end = {}
            for child in node.children:
                child_start, child_end = thompson_construction(child)
                start['EPSILON'] = start.get('EPSILON', []) + [child_start]
                child_end['EPSILON'] = [end]
            return start, end

        elif node.type == 'KLEENE':
            start = {}
            end = {}
            child_start, child_end = thompson_construction(node.children[0])
            start['EPSILON'] = [child_start, end]
            child_end['EPSILON'] = [child_start, end]
            return start, end

        elif node.type == 'PLUS':
            child_start, child_end = thompson_construction(node.children[0])
            start = {}
            end = {}
            start['EPSILON'] = [child_start]
            child_end['EPSILON'] = [child_start, end]
            return start, end

        elif node.type == 'OPTIONAL':
            start = {}
            end = {}
            child_start, child_end = thompson_construction(node.children[0])
            start['EPSILON'] = [child_start, end]
            child_end['EPSILON'] = [end]
            return start, end

        else:
            raise ValueError(f"Unrecognized node type: {node.type}")

    def convert_to_dict(start_state, end_state):
        state_counter = 0
        state_map = {}
        result = {}

        def get_state_id(state):
            nonlocal state_counter
            if id(state) not in state_map:
                state_map[id(state)] = f'S{state_counter}'
                state_counter += 1
            return state_map[id(state)]

        def traverse(state):
            state_id = get_state_id(state)
            if state_id in result:
                return
            result[state_id] = {}
            for symbol, next_states in state.items():
                result[state_id][symbol] = [get_state_id(next_state) for next_state in next_states]
                for next_state in next_states:
                    traverse(next_state)

        traverse(start_state)
        final_state_id = get_state_id(end_state)
        result[final_state_id] = {}
        return result

    # Procesar la notación postfix y construir el árbol de nodos
    regex_tree = thompson_construction_postfix(postfix)

    # Construir el AFN utilizando la construcción de Thompson
    afn_start, afn_end = thompson_construction(regex_tree)

    # Crear los estados inicial y final del AFN
    initial_state = {}
    initial_state['EPSILON'] = [afn_start]
    final_state = {}

    afn_end['EPSILON'] = [final_state]

    # Convertir el AFN a un diccionario de estados
    afn_dict = convert_to_dict(initial_state, final_state)

    # Identificar los estados de aceptación
    accepting_states = {state for state, transitions in afn_dict.items() if not transitions}

    # Marcar los estados de aceptación
    result_afn = {}
    for state, transitions in afn_dict.items():
        acceptance_mark = "*" if state in accepting_states else ""
        result_afn[f"{state}{acceptance_mark}"] = transitions

    return result_afn
