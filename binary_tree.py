"""Binary Search Tree"""

from flask import Blueprint, jsonify, render_template, request

binary_tree_bp = Blueprint("binary_tree", __name__)


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinaryTree:
    """Binary Search Tree with the three required methods."""

    def search(self, root, key):
        if root is None or root.value == key:
            return root
        if key < root.value:
            return self.search(root.left, key)
        return self.search(root.right, key)

    def post_traversal(self, start, traversal):
        if start is not None:
            self.post_traversal(start.left, traversal)
            self.post_traversal(start.right, traversal)
            traversal.append(start.value)
        return traversal

    def delete_node(self, root, key):
        if root is None:
            return None
        if key < root.value:
            root.left = self.delete_node(root.left, key)
        elif key > root.value:
            root.right = self.delete_node(root.right, key)
        else:
            if root.left is None:
                return root.right
            if root.right is None:
                return root.left
            successor = root.right
            while successor.left is not None:
                successor = successor.left
            root.value = successor.value
            root.right = self.delete_node(root.right, successor.value)
        return root

    def insert(self, root, key):
        if root is None:
            return Node(key)
        if key < root.value:
            root.left = self.insert(root.left, key)
        elif key > root.value:
            root.right = self.insert(root.right, key)
        return root


bst = BinaryTree()


def build_tree(values):
    root = None
    for value in values:
        root = bst.insert(root, value)
    return root


def serialize_tree(root):
    if root is None:
        return None
    return {
        "value": root.value,
        "left": serialize_tree(root.left),
        "right": serialize_tree(root.right),
    }


def preorder_values(root):
    """Return an insertion order that recreates the same BST shape."""
    if root is None:
        return []
    return [root.value] + preorder_values(root.left) + preorder_values(root.right)


def is_valid_number(value):
    return isinstance(value, int) and not isinstance(value, bool) and -9999 <= value <= 9999


@binary_tree_bp.get("/binary-tree")
def binary_tree():
    return render_template("binary-tree.html")


@binary_tree_bp.post("/binary-tree/api")
def binary_tree_api():
    data = request.get_json(silent=True) or {}
    action = data.get("action")
    values = data.get("values", [])
    key = data.get("key")

    if not isinstance(values, list) or len(values) > 200:
        return jsonify(error="Invalid tree values."), 400
    if not all(is_valid_number(value) for value in values):
        return jsonify(error="Tree values must be whole numbers from -9999 to 9999."), 400

    values = list(dict.fromkeys(values))
    root = build_tree(values)

    if action in ("insert", "search", "delete_node") and not is_valid_number(key):
        return jsonify(error="Enter a whole number from -9999 to 9999."), 400

    if action == "insert":
        if bst.search(root, key) is not None:
            message = f"{key} is already in the tree. Duplicate values are not allowed."
        else:
            root = bst.insert(root, key)
            values.append(key)
            message = f"Inserted {key} into the Binary Search Tree."
    elif action == "search":
        message = f"Found {key} in the tree." if bst.search(root, key) else f"{key} was not found in the tree."
    elif action == "delete_node":
        if bst.search(root, key) is None:
            message = f"{key} was not found. Nothing was deleted."
        else:
            root = bst.delete_node(root, key)
            values.remove(key)
            message = f"Deleted {key} from the Binary Search Tree."
    elif action == "post_traversal":
        message = "Postorder traversal: Left → Right → Root."
    elif action == "clear":
        root, values = None, []
        message = "The Binary Search Tree has been cleared."
    else:
        return jsonify(error="Unknown action."), 400

    return jsonify(
        values=preorder_values(root),
        tree=serialize_tree(root),
        postorder=bst.post_traversal(root, []),
        message=message,
    )


def register_binary_tree_routes(app):
    """Register the Binary Search Tree page and API routes on Flask."""
    app.register_blueprint(binary_tree_bp)
