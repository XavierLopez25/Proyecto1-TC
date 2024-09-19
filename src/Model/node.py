class Node:
    def __init__(self, type, children=None, value=None):
        self.type = type
        self.children = children if children else []
        self.value = value

    def __str__(self):
        if self.type == 'CHAR':
            return self.value
        elif self.type == 'KLEENE':
            return f"{str(self.children[0])}*"
        elif self.type == 'PLUS':
            return f"{str(self.children[0])}+"
        elif self.type == 'OPTIONAL':
            return f"{str(self.children[0])}?"
        elif self.type == 'CONCAT':
            return '.'.join(str(child) for child in self.children)
        elif self.type == 'ALTERNATE':
            return '|'.join(str(child) for child in self.children)
        return 'Undefined'
