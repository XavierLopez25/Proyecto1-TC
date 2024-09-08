import re
import pprint
from Controller.shunting_yard import shunting_yard_regex
from Controller.thompson import regex_to_nfa_thompson
from Controller.subset_construction import subset_construction

def main():
    allowed_characters = re.compile(r'^[a-zA-Z()|+*#]*$')

    expression = input("Enter a regex expression (only characters allowed: ),(,*,+,| and letters): ")
    verbose = input("Enable verbose mode? (yes/no): ").lower() == 'yes'
    
    if allowed_characters.match(expression):
        postfix = shunting_yard_regex(expression, verbose)
        afn_thompson = regex_to_nfa_thompson(expression, verbose)
        print("Postfix:", postfix)
        print("AFN w/ Thompson:")
        pprint.pprint(afn_thompson)

        start_state = 'S0'
        afd = subset_construction(afn_thompson, start_state)
        print('Resulting AFD: ')
        pprint.pprint(afd, width=1) 
    else:
        print("Invalid input. Please use only the allowed characters.")

if __name__ == "__main__":
    main()
