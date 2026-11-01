from flask import Flask, jsonify, render_template, request
import math
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

# Works pages na gumagamit ng parehong website frame at theme.
@app.route("/queue")
def queue():
    return render_template("queue.html", title="Queue",
                           max_items=MAX_ITEMS, max_length=MAX_VALUE_LENGTH)


@app.route("/deque")
def deque():
    return render_template("deque.html", title="Deque",
                           max_items=MAX_ITEMS, max_length=MAX_VALUE_LENGTH)


@app.route("/sorting")
def sorting():
    return render_template("sorting.html", title="Sorting", algorithms=SORTING_INFO,
                           references=REFERENCES)


# Python ang nagpapatakbo ng operations; ibinabalik ang state sa current page.
@app.route("/api/structures/<kind>", methods=["POST"])
def structures_api(kind):
    if request.content_length and request.content_length > 16000:
        return jsonify(error="This request is too large for the demo."), 400
    try:
        return jsonify(structure_action(kind, request.get_json(silent=True)))
    except ValueError as exception:
        return jsonify(error=str(exception)), 400


@app.route("/api/sorting", methods=["POST"])
def sorting_api():
    if request.content_length and request.content_length > 16000:
        return jsonify(error="This request is too large for the demo."), 400
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error="Enter numbers and choose an algorithm."), 400
    try:
        return jsonify(sort_numbers(payload.get("numbers"), payload.get("algorithm", "bubble"),
                                    payload.get("order", "asc")))
    except ValueError as exception:
        return jsonify(error=str(exception)), 400

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

# Queue, Deque at sorting logic para sa bagong Works tools.
MAX_ITEMS = 12
MAX_VALUE_LENGTH = 32
MAX_SORT_ITEMS = 20


class DequeNode:
    # May links sa previous at next para puwedeng mag-remove sa magkabilang dulo.
    def __init__(self, value):
        self.value = value
        self.previous = None
        self.next = None


class Deque:
    def __init__(self, values=()):
        self.front = None
        self.rear = None
        self.size = 0
        for value in values:
            self.add_rear(value)

    def add_front(self, value):
        node = DequeNode(value)
        node.next = self.front
        if self.front:
            self.front.previous = node
        else:
            self.rear = node
        self.front = node
        self.size += 1

    def add_rear(self, value):
        node = DequeNode(value)
        node.previous = self.rear
        if self.rear:
            self.rear.next = node
        else:
            self.front = node
        self.rear = node
        self.size += 1

    def remove_front(self):
        value = self.peek_front()
        self.front = self.front.next
        if self.front:
            self.front.previous = None
        else:
            self.rear = None
        self.size -= 1
        return value

    def remove_rear(self):
        value = self.peek_rear()
        self.rear = self.rear.previous
        if self.rear:
            self.rear.next = None
        else:
            self.front = None
        self.size -= 1
        return value

    def peek_front(self):
        if self.front is None:
            raise ValueError("The deque is empty. Add an item first.")
        return self.front.value

    def peek_rear(self):
        if self.rear is None:
            raise ValueError("The deque is empty. Add an item first.")
        return self.rear.value

    def clear(self):
        self.front = self.rear = None
        self.size = 0

    def values(self):
        current = self.front
        result = []
        while current:
            result.append(current.value)
            current = current.next
        return result


class Queue:
    # FIFO: sa rear ang enqueue at sa front ang dequeue.
    def __init__(self, values=()):
        self.items = Deque(values)

    def enqueue(self, value):
        self.items.add_rear(value)

    def dequeue(self):
        if not self.items.size:
            raise ValueError("The queue is empty. Enqueue an item first.")
        return self.items.remove_front()

    def peek(self):
        if not self.items.size:
            raise ValueError("The queue is empty. Enqueue an item first.")
        return self.items.peek_front()

    def clear(self):
        self.items.clear()

    def values(self):
        return self.items.values()


def structure_action(kind, payload):
    # Current page state lang ang binabasa; walang shared list sa ibang visitors.
    if kind not in {"queue", "deque"}:
        raise ValueError("Choose queue or deque.")
    if not isinstance(payload, dict):
        raise ValueError("Send a valid operation.")
    values = payload.get("values", [])
    if not isinstance(values, list) or len(values) > MAX_ITEMS:
        raise ValueError(f"Use at most {MAX_ITEMS} items in this demo.")
    if any(not isinstance(value, str) or not value.strip() or
           len(value) > MAX_VALUE_LENGTH for value in values):
        raise ValueError(f"Each item needs 1–{MAX_VALUE_LENGTH} characters.")
    action = payload.get("action")
    allowed = ({"enqueue", "dequeue", "peek", "clear"} if kind == "queue" else
               {"add_front", "add_rear", "remove_front", "remove_rear",
                "peek_front", "peek_rear", "clear"})
    if not isinstance(action, str) or action not in allowed:
        raise ValueError("Choose one of the available operations.")
    value = payload.get("value", "")
    if action in {"enqueue", "add_front", "add_rear"}:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Enter an item value first.")
        value = value.strip()
        if len(value) > MAX_VALUE_LENGTH:
            raise ValueError(f"Use at most {MAX_VALUE_LENGTH} characters per item.")
        if len(values) == MAX_ITEMS:
            raise ValueError(f"This demo holds {MAX_ITEMS} items. Remove one before adding another.")
    structure = Queue(values) if kind == "queue" else Deque(values)
    result = getattr(structure, action)(value) if action in {
        "enqueue", "add_front", "add_rear"} else getattr(structure, action)()
    if action in {"enqueue", "add_front", "add_rear"}:
        end = "front" if action == "add_front" else "rear"
        message = f'Added “{value}” at the {end}.'
    elif action in {"dequeue", "remove_front", "remove_rear"}:
        end = "rear" if action == "remove_rear" else "front"
        message = f'Removed “{result}” from the {end}.'
    elif action.startswith("peek"):
        end = "rear" if action == "peek_rear" else "front"
        message = f'The {end} item is “{result}”. No item was removed.'
    else:
        message = f"Your {kind} is now empty."
    updated = structure.values()
    return {"values": updated, "size": len(updated),
            "front": updated[0] if updated else None,
            "rear": updated[-1] if updated else None, "message": message}


REFERENCES = [
    {"id": "overview", "title": "Sorting", "author": "Robert Sedgewick & Kevin Wayne",
     "publisher": "Princeton University · Algorithms, 4th Edition",
     "url": "https://algs4.cs.princeton.edu/20sorting/"},
    {"id": "elementary", "title": "Elementary Sorts", "author": "Robert Sedgewick & Kevin Wayne",
     "publisher": "Princeton University · Algorithms, 4th Edition",
     "url": "https://algs4.cs.princeton.edu/21elementary/"},
    {"id": "summary", "title": "Algorithms and Data Structures Cheatsheet",
     "author": "Robert Sedgewick & Kevin Wayne", "publisher": "Princeton University",
     "url": "https://algs4.cs.princeton.edu/cheatsheet/"},
    {"id": "merge", "title": "Mergesort", "author": "Robert Sedgewick & Kevin Wayne",
     "publisher": "Princeton University · Algorithms, 4th Edition",
     "url": "https://algs4.cs.princeton.edu/22mergesort/"},
    {"id": "quick", "title": "Quicksort", "author": "Robert Sedgewick & Kevin Wayne",
     "publisher": "Princeton University · Algorithms, 4th Edition",
     "url": "https://algs4.cs.princeton.edu/23quicksort/"},
]

SORTING_INFO = {
    "bubble": {
        "name": "Bubble Sort", "tagline": "Compare neighbors. Swap. Repeat.",
        "description": "Bubble Sort compares neighboring values and swaps pairs that are out of order. Each pass moves the largest remaining value to the end in ascending order.",
        "steps": ["Compare two neighbors.", "Swap them if their order is wrong.",
                  "Repeat with a shorter unsorted section; stop early if no swaps occur."],
        "best": "O(n)", "average": "O(n²)", "worst": "O(n²)", "space": "O(1)",
        "stable": "Yes", "use": "Useful for learning comparisons and swaps on small lists.",
        "note": "The linear best case assumes the early-stop check used in this demo.",
        "source": "summary",
    },
    "selection": {
        "name": "Selection Sort", "tagline": "Find the next smallest value.",
        "description": "Selection Sort searches the unsorted section for its smallest value, then swaps that value into the next position. For descending order it selects the largest instead.",
        "steps": ["Search the unsorted section for its smallest value.",
                  "Swap it with the first unsorted position.", "Move the boundary right and repeat."],
        "best": "O(n²)", "average": "O(n²)", "worst": "O(n²)", "space": "O(1)",
        "stable": "No", "use": "Makes few swaps, but still scans the unsorted section each time.",
        "note": "Already sorted input still needs quadratic comparisons.", "source": "elementary",
    },
    "insertion": {
        "name": "Insertion Sort", "tagline": "Build a sorted section, one item at a time.",
        "description": "Insertion Sort takes the next value and moves it into the correct position within the sorted section on its left, similar to arranging playing cards.",
        "steps": ["Treat the first item as the sorted section.",
                  "Move the next item left past larger values.", "Repeat until every item is inserted."],
        "best": "O(n)", "average": "O(n²)", "worst": "O(n²)", "space": "O(1)",
        "stable": "Yes", "use": "A useful choice for small or nearly sorted lists.",
        "note": "Equal values are not swapped, preserving their original order.", "source": "elementary",
    },
    "merge": {
        "name": "Merge Sort", "tagline": "Divide the list, then merge it in order.",
        "description": "Merge Sort divides a list into smaller halves, sorts each half, and combines the sorted halves by repeatedly choosing the next value in order.",
        "steps": ["Split the list until each section has one item.",
                  "Compare the front values of two sorted sections.", "Merge in order and repeat upward."],
        "best": "O(n log n)", "average": "O(n log n)", "worst": "O(n log n)", "space": "O(n)",
        "stable": "Yes", "use": "Provides a guaranteed O(n log n) time bound and preserves equal-key order.",
        "note": "This standard array version needs an auxiliary array.", "source": "merge",
    },
    "quick": {
        "name": "Quick Sort", "tagline": "Choose a pivot and partition around it.",
        "description": "Quick Sort chooses a pivot, partitions values around it, then recursively sorts the two sides. This demo uses the last value of each section as its pivot.",
        "steps": ["Choose the final item of the section as pivot.",
                  "Move smaller values before the pivot for ascending order.",
                  "Place the pivot, then sort the left and right sections."],
        "best": "O(n log n)", "average": "O(n log n)", "worst": "O(n²)",
        "space": "O(log n) average; O(n) worst", "stable": "No",
        "use": "Often fast in practice; pivot choices affect performance.",
        "note": "Average time assumes randomly ordered input. Last-item pivots can give quadratic time on sorted or equal-value lists.",
        "source": "quick",
    },
}


def parse_numbers(raw):
    if not isinstance(raw, str) or not raw.strip():
        raise ValueError("Enter some numbers first. Example: 8, 3, 5, 1, 4.")
    if len(raw) > 600:
        raise ValueError("Keep your input within 600 characters.")
    if any(not part.strip() for part in raw.strip().split(",")):
        raise ValueError("Add a number between commas and remove any trailing comma.")
    tokens = re.split(r"[\s,]+", raw.strip())
    if len(tokens) > MAX_SORT_ITEMS:
        raise ValueError(f"Use at most {MAX_SORT_ITEMS} numbers for the step-by-step demo.")
    numbers = []
    for token in tokens:
        if not re.fullmatch(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", token):
            raise ValueError(f'“{token}” is not a valid number. Separate numbers with commas or spaces.')
        value = float(token)
        if not math.isfinite(value) or abs(value) > 1_000_000_000:
            raise ValueError("Use finite numbers between −1,000,000,000 and 1,000,000,000.")
        numbers.append(int(value) if value.is_integer() else value)
    return numbers


def sort_numbers(raw, algorithm="bubble", order="asc"):
    if not isinstance(algorithm, str) or algorithm not in SORTING_INFO:
        raise ValueError("Choose a sorting algorithm from the list.")
    if order not in ("asc", "desc"):
        raise ValueError("Choose ascending or descending order.")
    array = parse_numbers(raw)
    original = array.copy()
    steps = []
    comparisons = writes = 0

    # Snapshot ng tunay na algorithm state para sa Previous, Next at Play.
    def record(message, active=(), pivot=None, done=False):
        steps.append({"values": array.copy(), "message": message,
                      "active": list(active), "pivot": pivot, "done": done,
                      "comparisons": comparisons, "writes": writes})

    def before(left, right):
        nonlocal comparisons
        comparisons += 1
        return left < right if order == "asc" else left > right

    def swap(left, right):
        nonlocal writes
        if left != right:
            array[left], array[right] = array[right], array[left]
            writes += 2

    record("Original list. Choose Next step or Play to follow the algorithm.")
    length = len(array)
    if algorithm == "bubble":
        for end in range(length - 1, 0, -1):
            changed = False
            for index in range(end):
                left, right = array[index], array[index + 1]
                if before(right, left):
                    swap(index, index + 1)
                    changed = True
                    message = f"Compare {left} and {right}: swap this pair."
                else:
                    message = f"Compare {left} and {right}: keep this pair."
                record(message, (index, index + 1))
            record(f"Pass complete. Position {end + 1} is now settled.")
            if not changed:
                record("No swaps in this pass. The list is already in order.")
                break
    elif algorithm == "selection":
        for start in range(length - 1):
            selected = start
            for candidate in range(start + 1, length):
                if before(array[candidate], array[selected]):
                    selected = candidate
                record(f"Scan position {candidate + 1}; current selection is {array[selected]}.",
                       (selected, candidate))
            swap(start, selected)
            record(f"Place {array[start]} at position {start + 1}.", (start, selected))
    elif algorithm == "insertion":
        # Adjacent swaps ang gamit para makita ang pag-usog ng bawat item.
        for start in range(1, length):
            current = start
            while current > 0:
                moving, previous = array[current], array[current - 1]
                move_left = before(moving, previous)
                if move_left:
                    swap(current, current - 1)
                    record(f"Move {moving} left past {previous}.", (current - 1, current))
                    current -= 1
                else:
                    record(f"Compare {previous} and {moving}: the insertion position is correct.",
                           (current - 1, current))
                    break
            record(f"The first {start + 1} items are sorted relative to each other.")
    elif algorithm == "merge":
        def merge_sort(low, high):
            nonlocal writes
            if high - low <= 1:
                return
            middle = (low + high) // 2
            record(f"Split positions {low + 1}–{high} into two sections.", range(low, high))
            merge_sort(low, middle)
            merge_sort(middle, high)
            left, right = array[low:middle], array[middle:high]
            i = j = 0
            for target in range(low, high):
                # Left muna kapag equal para stable ang merge.
                if i < len(left) and (j == len(right) or not before(right[j], left[i])):
                    value = left[i]
                    i += 1
                else:
                    value = right[j]
                    j += 1
                array[target] = value
                writes += 1
                record(f"Merge: copy {value} from the temporary halves to position {target + 1}.", (target,))
            record(f"Positions {low + 1}–{high} are now merged in order.", range(low, high))
        merge_sort(0, length)
    else:
        def quick_sort(low, high):
            if low >= high:
                return
            pivot = array[high]
            boundary = low
            record(f"Choose {pivot} at position {high + 1} as pivot.", (high,), high)
            for current in range(low, high):
                value = array[current]
                if before(value, pivot):
                    swap(boundary, current)
                    record(f"Compare {value} with pivot {pivot}: move it to the left partition.",
                           (boundary, current), high)
                    boundary += 1
                else:
                    record(f"Compare {value} with pivot {pivot}: keep it in the right partition.",
                           (current,), high)
            swap(boundary, high)
            record(f"Pivot {pivot} is settled at position {boundary + 1}.", (boundary,), boundary)
            quick_sort(low, boundary - 1)
            quick_sort(boundary + 1, high)
        quick_sort(0, length - 1)
    record("Sorting complete. Every value is in the requested order.", done=True)
    return {"original": original, "result": array, "steps": steps,
            "comparisons": comparisons, "writes": writes,
            "algorithm": algorithm, "order": order}

# Simulan ang local website sa http://127.0.0.1:8000/.
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
