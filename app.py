from flask import Flask, render_template, request
import re

# Gumawa ng Flask app; dito naka-connect ang templates at static files.
app = Flask(__name__)

# I-open ang index page gamit ang Flask route.
@app.route("/")
def index():
    return render_template("index.html")

# I-open ang profile page gamit ang Flask route.
@app.route("/profile")
def profile():
    return render_template("profile.html")

# I-open ang contact page gamit ang Flask route.
@app.route("/contact")
def contact():
    return render_template("contact.html")

# I-open ang works page gamit ang Flask route.
@app.route("/works")
def works():
    return render_template("works.html")

# I-open ang uppercase page gamit ang Flask route.
@app.route("/uppercase")
def uppercase():
    return render_template("uppercase.html")

# I-open ang triangle page gamit ang Flask route.
@app.route("/triangle")
def triangle():
    return render_template("triangle.html")

# I-open ang circle page gamit ang Flask route.
@app.route("/circle")
def circle():
    return render_template("circle.html")

# I-open ang linked-list page gamit ang Flask route.
@app.route("/linked-list")
def linked_list():
    return render_template("linked-list.html")


# Node ang lalagyan ng token at link sa kasunod na node.
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

# Linked list para sa operator stack at postfix output.
class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    # Push sa head para last-in, first-out ang operators.
    def push(self, value):
        node = Node(value)
        node.next = self.head
        self.head = node
        if self.tail is None:
            self.tail = node

    # Pop ang top node at ibalik ang token nito.
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

    # Append sa tail para manatili ang postfix order.
    def append(self, value):
        node = Node(value)
        if self.tail:
            self.tail.next = node
        else:
            self.head = node
        self.tail = node

    # Traverse ang nodes para maipakita ang tokens sa UI.
    def values(self):
        current = self.head
        while current:
            yield current.value
            current = current.next

# Shunting Yard conversion gamit ang linked list na may nodes.
def infix_to_postfix(expression):
    if not isinstance(expression, str) or not expression.strip():
        raise ValueError("Enter an infix expression first.")
    if len(expression) > 500:
        raise ValueError("Use an expression with at most 500 characters.")
    tokens = []
    position = 0
    pattern = re.compile(r"\s*(?:(\d+(?:\.\d+)?|\.\d+)|([A-Za-z_][A-Za-z_0-9]*)|([()+*/^\-]))")
    # Basahin ang bawat token; tanggihan ang unsupported characters.
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

    # Snapshot ng stack at output pagkatapos ng bawat action.
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
            # Equal precedence pops, maliban sa right-associative exponent ^.
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

# I-open ang page at i-convert ang expression sa Python backend.
@app.route("/infix-postfix", methods=["GET", "POST"])
def infix_postfix():
    expression, postfix, nodes, steps, error = "", "", [], [], ""
    if request.method == "POST":
        expression = request.form.get("expression", "")
        try:
            postfix, nodes, steps = infix_to_postfix(expression)
        except ValueError as exception:
            error = str(exception)
    return render_template("infix-postfix.html", expression=expression,
                           postfix=postfix, nodes=nodes, steps=steps, error=error)

# Simulan ang local website sa http://127.0.0.1:8000/.
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
