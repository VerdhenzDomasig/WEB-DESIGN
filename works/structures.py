MAX_ITEMS = 12
MAX_VALUE_LENGTH = 32


class DequeNode:
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
