import re
import pprint
#instalen graphviz con pip install graphviz
from graphviz import Digraph
from Controller.shunting_yard import shunting_yard_regex
from Controller.thompson import regex_to_nfa_thompson
from Controller.subset_construction import subset_construction
from Controller.hopcroft import hopcroft_minimization


def graficar_automata(automata, nombre='Automata'):

    dot = Digraph(name=nombre, format='png')  # Puedes cambiar el formato si lo deseas
    dot.attr(rankdir='LR')  # Orientación de izquierda a derecha

    estados_finales = set()
    estados_iniciales = set(automata.keys())

    # Añadir nodos
    for estado in automata:
        if estado.endswith('*'):
            nombre_estado = estado.rstrip('*')
            dot.node(nombre_estado, nombre_estado, shape='doublecircle')
            estados_finales.add(nombre_estado)
        else:
            dot.node(estado, estado, shape='circle')

    # Opcional: Añadir un nodo inicial sin forma y una flecha hacia el estado inicial
    dot.node('', shape='none')  # Nodo invisible
    if automata:
        primer_estado = list(automata.keys())[0]
        dot.edge('', primer_estado)

    # Añadir transiciones
    for estado, transiciones in automata.items():
        origen = estado.rstrip('*') 
        for simbolo, destinos in transiciones.items():
            if isinstance(destinos, list):
                for destino in destinos:
                    destino_nombre = destino.rstrip('*')
                    etiqueta = simbolo
                    if simbolo == 'EPSILON':
                        etiqueta = 'ε'
                    dot.edge(origen, destino_nombre, label=etiqueta)
            elif isinstance(destinos, str):
                destino_nombre = destinos.rstrip('*')
                etiqueta = simbolo
                if simbolo == 'EPSILON':
                    etiqueta = 'ε'
                dot.edge(origen, destino_nombre, label=etiqueta)
            elif destinos is None:
                pass  # No hay transición para este símbolo
            else:
                raise ValueError(f"Formato de destino no reconocido: {destinos}")

    # Renderizar el grafo
    dot.render(nombre, view=True)


def main():
    allowed_characters = re.compile(r'^[a-zA-Z()|+*#]*$')

    print("Welcome to the regex to minimized AFD converter \n Please enter a regex expression and choose if you want to enable verbose mode")
    print("The syntax acepted are: \n - ( ) for grouping \n - | for OR \n - + for Kleene sum  \n - * for Kleene star \n - # for  \n - 0-9 for numbers")

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
        graficar_automata(afn_thompson, 'AFN Thompson')

        start_state = 'S0'
        afd = subset_construction(afn_thompson, start_state)
        print('Resulting AFD: ')
        pprint.pprint(afd, width=1)

        # Generar la imagen del AFD
        graficar_automata(afd, 'AFD')

        print('Minimized AFD: ')
        minimized_afd = hopcroft_minimization(afd)
        pprint.pprint(minimized_afd, width=1)

        # Generar la imagen del AFD minimizado
        graficar_automata(minimized_afd, 'Minimized AFD')

    else:
        print("Invalid input. Please use only the allowed characters.")

if __name__ == "__main__":
    main()
