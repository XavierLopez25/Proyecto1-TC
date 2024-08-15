import re
from shunting_yard import shunting_yard_regex
from thompson import regex_to_nfa_thompson
import pprint

def main():
    allowed_characters = re.compile(r'^[a-zA-Z()#+*]*$')
    
    expression = input("Enter a regex expression (only characters allowed: ),(,*,+, and letters): ")
        
    if allowed_characters.match(expression):
        postfix = shunting_yard_regex(expression)
        afn_thompson = regex_to_nfa_thompson(expression)
        print("Postfix:", postfix)
        print("AFN w/ Thompson:")
        pprint.pprint(afn_thompson)
    else:
        print("Invalid input. Please use only the allowed characters.")


if __name__ == "__main__":
    main()
