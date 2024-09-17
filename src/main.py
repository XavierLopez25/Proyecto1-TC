import re
import pprint
#instalen graphviz con pip install graphviz
import graphviz
from Controller.shunting_yard import shunting_yard_regex
from Controller.thompson import regex_to_nfa_thompson
from Controller.subset_construction import subset_construction
from Controller.hopcroft import hopcroft_minimization

def generate_graph(fsm, title, filename):
    dot = graphviz.Digraph(comment=title)
    
    for state, transitions in fsm.items():
        # Marcar los estados de aceptación (que contienen '*') con doble círculo, pero manteniendo el mismo nombre de estado
        if '*' in state:
            dot.node(state, shape='doublecircle', label=state.replace('*', ''))  # Marcar como estado de aceptación
        else:
            dot.node(state, shape='circle', label=state)  # Estado normal
        
        for symbol, targets in transitions.items():
            if targets is not None:
                # Verificar si el destino es una lista (como en el caso de epsilon-transiciones)
                if isinstance(targets, list):
                    for target in targets:
                        dot.edge(state, target.replace('*', ''), label=symbol)  # Eliminar '*' de los destinos
                else:
                    # Si es un solo estado de destino
                    dot.edge(state, targets.replace('*', ''), label=symbol)  # Eliminar '*' de los destinos
    
    # Guardar y visualizar
    dot.render(f'{filename}.gv', format='png', view=True)

def main():
    allowed_characters = re.compile(r'^[a-zA-Z()|+*#]*$')

    expression = input("Enter a regex expression (only characters allowed: ),(,*,+,| and letters): ")
    verbose = input("Enable verbose mode? (yes/no): ").lower() == 'yes'

    # expression = "((b|a)d|d)"
    # verbose = "yes"
    if allowed_characters.match(expression):
        postfix = shunting_yard_regex(expression, verbose)
        afn_thompson = regex_to_nfa_thompson(expression, verbose)
        print("Postfix:", postfix)
        print("AFN w/ Thompson:")
        pprint.pprint(afn_thompson)

        # Generar la imagen del AFN
        # generate_graph(afn_thompson, 'AFN Thompson', 'afn_thompson')

        start_state = 'S0'
        afd = subset_construction(afn_thompson, start_state)
        print('Resulting AFD: ')
        pprint.pprint(afd, width=1)

        # Generar la imagen del AFD
        # generate_graph(afd, 'AFD', 'afd')

        print('Minimized AFD: ')
        minimized_afd = hopcroft_minimization(afd)
        pprint.pprint(minimized_afd, width=1)

        # Generar la imagen del AFD minimizado
        # generate_graph(minimized_afd, 'Minimized AFD', 'minimized_afd')
    else:
        print("Invalid input. Please use only the allowed characters.")

if __name__ == "__main__":
    main()
