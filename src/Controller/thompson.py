from src.Model.node import Node


def regex_to_nfa_thompson(expression):
    def parse_regex(expression):
        tokens = list(expression.replace(' ', ''))
        i = 0

        def parse_term():
            nonlocal i
            if i >= len(tokens):
                return None
            if tokens[i] == '(':
                i += 1
                subexpr = parse_expression()
                if i < len(tokens) and tokens[i] == ')':
                    i += 1
                    return subexpr
                else:
                    raise ValueError("Paréntesis desbalanceados")
            elif tokens[i].isalpha() or tokens[i] == '#':
                char = tokens[i]
                i += 1
                return Node('CHAR', value=char)
            else:
                raise ValueError(f"Token inesperado: {tokens[i]}")

        def parse_factor():
            nonlocal i
            node = parse_term()
            while i < len(tokens) and tokens[i] in '*+?':
                if tokens[i] == '*':
                    node = Node('KLEENE', [node])
                elif tokens[i] == '+':
                    node = Node('PLUS', [node])
                elif tokens[i] == '?':
                    node = Node('OPTIONAL', [node])
                i += 1
            return node

        def parse_concat():
            nonlocal i
            nodes = []
            while i < len(tokens) and tokens[i] not in '|)':
                nodes.append(parse_factor())
            if len(nodes) == 1:
                return nodes[0]
            return Node('CONCAT', nodes)

        def parse_expression():
            nonlocal i
            node = parse_concat()
            while i < len(tokens) and tokens[i] == '|':
                i += 1
                node = Node('ALTERNATE', [node, parse_concat()])
            return node

        return parse_expression()

    def thompson_construction(node):
        if node.type == 'CHAR':
            start = {}
            end = {}
            start[node.value] = [end]
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

    regex = parse_regex(expression)

    afn_start, afn_end = thompson_construction(regex)

    initial_state = {}
    initial_state['EPSILON'] = [afn_start]
    final_state = {}

    afn_end['EPSILON'] = [final_state]

    afn_dict = convert_to_dict(initial_state, final_state)

    return afn_dict