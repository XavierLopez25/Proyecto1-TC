import re
import pprint
#instalen graphviz con pip install graphviz
from graphviz import Digraph
from Controller.shunting_yard import shunting_yard_regex
from Controller.thompson import regex_to_nfa_thompson
from Controller.subset_construction import subset_construction
from Controller.hopcroft import hopcroft_minimization
import os

header = """
██╗    ██╗███████╗██╗      ██████╗ ██████╗ ███╗   ███╗███████╗    ████████╗ ██████╗     ██████╗ ███████╗ ██████╗ ███████╗██╗  ██╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ███████╗██████╗ 
██║    ██║██╔════╝██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝    ╚══██╔══╝██╔═══██╗    ██╔══██╗██╔════╝██╔════╝ ██╔════╝╚██╗██╔╝╚════██╗████╗ ████║██║████╗  ██║██╔══██╗██╔════╝██╔══██╗
██║ █╗ ██║█████╗  ██║     ██║     ██║   ██║██╔████╔██║█████╗         ██║   ██║   ██║    ██████╔╝█████╗  ██║  ███╗█████╗   ╚███╔╝  █████╔╝██╔████╔██║██║██╔██╗ ██║███████║█████╗  ██║  ██║
██║███╗██║██╔══╝  ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝         ██║   ██║   ██║    ██╔══██╗██╔══╝  ██║   ██║██╔══╝   ██╔██╗ ██╔═══╝ ██║╚██╔╝██║██║██║╚██╗██║██╔══██║██╔══╝  ██║  ██║
╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗       ██║   ╚██████╔╝    ██║  ██║███████╗╚██████╔╝███████╗██╔╝ ██╗███████╗██║ ╚═╝ ██║██║██║ ╚████║██║  ██║██║     ██████╔╝
 ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝       ╚═╝    ╚═════╝     ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═════╝ 
"""

def graficar_automata(automata, nombre='Automata', estado_inicial=None):
    dot = Digraph(name=nombre, format='png')
    dot.attr(rankdir='LR')

    estados_finales = set()
    for estado in automata:
        if estado.endswith('*'):
            nombre_estado = estado.rstrip('*')
            dot.node(nombre_estado, nombre_estado, shape='doublecircle')
            estados_finales.add(nombre_estado)
        else:
            dot.node(estado, estado, shape='circle')

    if estado_inicial is None:
        estado_inicial = list(automata.keys())[0]

    # Asegurarse de que el estado inicial no termine en '*' para los casos de estados de aceptación
    estado_inicial = estado_inicial.rstrip('*')

    # Nodo inicial invisible y flecha hacia el estado inicial real
    dot.node('', shape='none')
    dot.edge('', estado_inicial, style='dashed')

    for estado, transiciones in automata.items():
        origen = estado.rstrip('*')
        for simbolo, destinos in transiciones.items():
            if isinstance(destinos, list):
                for destino in destinos:
                    destino_nombre = destino.rstrip('*')
                    etiqueta = 'ε' if simbolo == 'EPSILON' else simbolo
                    dot.edge(origen, destino_nombre, label=etiqueta)
            elif isinstance(destinos, str):
                destino_nombre = destinos.rstrip('*')
                etiqueta = 'ε' if simbolo == 'EPSILON' else simbolo
                dot.edge(origen, destino_nombre, label=etiqueta)
            elif destinos is None:
                continue  # No hay transición para este símbolo
            else:
                raise ValueError(f"Formato de destino no reconocido: {destinos}")

    dot.render(nombre, view=True)



def main():
    allowed_characters = re.compile(r'^[a-zA-Z0-9()|+*#]*$')
    os.system('cls' if os.name == 'nt' else 'clear')
    print(header)
    print("🔳"*93,"\n")
    print("Please enter a regex expression and choose if you want to enable verbose mode")
    print("The syntax acepted are: \n - ( ) for grouping \n - | for OR \n - + for Kleene sum  \n - * for Kleene star \n - # for  \n - 0-9 for numbers \n")
    print("🔳"*93,"\n")

    expression = input("Enter a regex expression (only characters allowed: ),(,*,+,| and letters): ")
    verbose = input("Enable verbose mode? (yes/no): ").lower() == 'yes'


    if allowed_characters.match(expression):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("🔳"*50,"\n")
        print("Trying this expression: ",expression,"\n")
        print("🔳"*50,"\n")

        print("PROCESS POSTFIX SHUNTING YARD\n")
        postfix = shunting_yard_regex(expression, verbose)
        print("Postfix:", postfix, "\n")

        print("🔳"*50,"\n")

        print("PROCESS AFN THOMPSON\n")
        afn_thompson = regex_to_nfa_thompson(expression, verbose)
        print("AFN w/ Thompson:")
        pprint.pprint(afn_thompson)
        print("\n")
        graficar_automata(afn_thompson, 'AFN Thompson')

        print("🔳"*50,"\n")

        print("PROCESS AFD SUBSET CONSTRUCTION\n")
        afd = subset_construction(afn_thompson, start_state='S0', verbose=verbose)
        print('AFD w/ Subset Constrution: ')
        pprint.pprint(afd, width=1)
        print("\n")
        graficar_automata(afd, 'AFD')

        print("🔳"*50,"\n")

        print("PROCESS MINIMIZED AFD HOPCROFT \n")
        minimized_afd = hopcroft_minimization(afd, verbose)
        print('Minimized AFD: ')
        pprint.pprint(minimized_afd, width=1)
        print("\n")
        graficar_automata(minimized_afd, 'Minimized AFD')

        print("🔳"*50,"\n")

    else:
        print("Invalid input. Please use only the allowed characters.")

if __name__ == "__main__":
    main()
