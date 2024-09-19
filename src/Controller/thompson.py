from Model.node import Node
from Controller.shunting_yard import shunting_yard_regex    

def parse_postfix(expression):
    stack = []
    tokens = list(expression)
    for token in tokens:
        if token.isalnum():
            stack.append(Node('CHAR', value=token))
        elif token in {'*', '+', '?'}:
            operand = stack.pop() if stack else Node('Undefined')
            node_type = {'*': 'KLEENE', '+': 'PLUS', '?': 'OPTIONAL'}[token]
            stack.append(Node(node_type, [operand]))
        elif token == '.':
            right = stack.pop() if stack else Node('Undefined')
            left = stack.pop() if stack else Node('Undefined')
            stack.append(Node('CONCAT', [left, right]))
        elif token == '|':
            right = stack.pop() if stack else Node('Undefined')
            left = stack.pop() if stack else Node('Undefined')
            stack.append(Node('ALTERNATE', [left, right]))
    return stack.pop() if stack else Node('Undefined')

def thompson_construction(node):
    if node.type == 'CHAR':
        start = {}
        end = {}
        start[node.value] = [end]
        return start, end
    elif node.type == 'CONCAT':
        left_start, left_end = thompson_construction(node.children[0])
        right_start, right_end = thompson_construction(node.children[1])
        left_end['EPSILON'] = [right_start]
        return left_start, right_end
    elif node.type == 'ALTERNATE':
        start = {}
        end = {}
        for child in node.children:
            child_start, child_end = thompson_construction(child)
            start.setdefault('EPSILON', []).append(child_start)
            child_end['EPSILON'] = [end]
        return start, end
    elif node.type == 'KLEENE':
        start = {}
        end = {}
        child_start, child_end = thompson_construction(node.children[0])
        start['EPSILON'] = [child_start, end]
        child_end['EPSILON'] = [start]
        return start, end
    elif node.type == 'PLUS':
        child_start, child_end = thompson_construction(node.children[0])
        child_end['EPSILON'] = [child_start]
        return child_start, child_end
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
        if state_id not in result:
            result[state_id] = {}
            for symbol, next_states in state.items():
                result[state_id][symbol] = [get_state_id(next_state) for next_state in next_states]
                for next_state in next_states:
                    traverse(next_state)

    traverse(start_state)
    final_state_id = get_state_id(end_state)
    # Agregar un asterisco al identificador del estado de aceptación para marcarlo claramente
    result[f"{final_state_id}*"] = result.pop(final_state_id)
    return result


def regex_to_nfa_thompson(expression, verbose=False):
    postfix_expression = shunting_yard_regex(expression, verbose)
    syntax_tree = parse_postfix(postfix_expression)
    if syntax_tree is None:
        if verbose:
            print("Syntax tree construction failed.")
        return None

    afn_start, afn_end = thompson_construction(syntax_tree)
    if afn_start is None or afn_end is None:
        if verbose:
            print("Thompson construction failed.")
        return None

    result_afn = convert_to_dict(afn_start, afn_end)
    return result_afn
