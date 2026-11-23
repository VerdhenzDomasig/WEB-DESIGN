import re

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def push(self, value):
        node = Node(value)
        node.next = self.head
        self.head = node
        if self.tail is None:
            self.tail = node

    def pop(self):
        if self.head is None:
            raise ValueError("The operator stack is empty.")
        value = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        return value

    def peek(self):
        return self.head.value if self.head else None

    def append(self, value):
        node = Node(value)
        if self.tail:
            self.tail.next = node
        else:
            self.head = node
        self.tail = node

    def values(self):
        current = self.head
        while current:
            yield current.value
            current = current.next

def infix_to_postfix(expression):
    if not isinstance(expression, str) or not expression.strip():
        raise ValueError("Enter an infix expression first.")
    if len(expression) > 500:
        raise ValueError("Use an expression with at most 500 characters.")
    tokens = []
    position = 0
    pattern = re.compile(r"\s*(?:(\d+(?:\.\d+)?|\.\d+)|([A-Za-z_][A-Za-z_0-9]*)|([()+*/^\-]))")
    
    while position < len(expression):
        if not expression[position:].strip():
            break
        match = pattern.match(expression, position)
        if not match:
            raise ValueError("Use numbers, variable names, parentheses, and + - * / ^ only.")
        tokens.append(next(group for group in match.groups() if group is not None))
        position = match.end()
    ops, output = LinkedList(), LinkedList()
    steps = []
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
    expecting_operand = True

    
    def record(token, action):
        steps.append({"token": token, "action": action,
                      "stack": " → ".join(ops.values()) or "empty",
                      "output": " ".join(output.values()) or "empty"})

    for token in tokens:
        if token == "(":
            if not expecting_operand:
                raise ValueError("Add an operator before '('. Example: A * (B + C).")
            ops.push(token)
            record(token, "Push opening parenthesis onto the operator stack.")
        elif token == ")":
            if expecting_operand:
                raise ValueError("A closing parenthesis must follow an operand; empty parentheses are invalid.")
            while ops.peek() is not None and ops.peek() != "(":
                value = ops.pop()
                output.append(value)
                record(token, f"Pop {value} from the stack and append it to output.")
            if ops.peek() is None:
                raise ValueError("Parentheses do not match: missing '('.")
            ops.pop()
            record(token, "Pop and discard the opening parenthesis.")
            expecting_operand = False
        elif token in precedence:
            if expecting_operand:
                raise ValueError("Each operator needs a left and right operand. Unary + or - is not supported; use (0 - A).")
            
            while (ops.peek() in precedence and
                   (precedence[ops.peek()] > precedence[token] or
                    (precedence[ops.peek()] == precedence[token] and token != "^"))):
                value = ops.pop()
                output.append(value)
                record(token, f"Pop {value} by precedence and append it to output.")
            ops.push(token)
            record(token, f"Push {token} onto the operator stack.")
            expecting_operand = True
        else:
            if not expecting_operand:
                raise ValueError("Add an operator between operands.")
            output.append(token)
            record(token, f"Append operand {token} to output.")
            expecting_operand = False
    if expecting_operand:
        raise ValueError("Complete the expression with an operand.")
    while ops.peek() is not None:
        value = ops.pop()
        if value == "(":
            raise ValueError("Parentheses do not match: missing ')'.")
        output.append(value)
        record("End", f"Pop remaining operator {value} and append it to output.")
    return " ".join(output.values()), list(output.values()), steps
