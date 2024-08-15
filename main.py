import re
from shunting_yard import shunting_yard_regex

def main():
    allowed_characters = re.compile(r'^[a-zA-Z()+*]*$')
    
    while True:
        expression = input("Enter a regex expression (only characters allowed: ),(,*,+, and letters): ")
        
        if allowed_characters.match(expression):
            postfix = shunting_yard_regex(expression)
            print("Postfix:", postfix)
        else:
            print("Invalid input. Please use only the allowed characters.")

if __name__ == "__main__":
    main()
