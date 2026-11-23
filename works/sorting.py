import math
import re


MAX_SORT_ITEMS = 20

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
