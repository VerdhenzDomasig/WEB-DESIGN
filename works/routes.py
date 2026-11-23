from flask import jsonify, render_template, request

from .infix_postfix import infix_to_postfix
from .sorting import REFERENCES, SORTING_INFO, sort_numbers
from .structures import MAX_ITEMS, MAX_VALUE_LENGTH, structure_action


def works():
    return render_template("works.html")


def queue():
    return render_template(
        "queue.html",
        title="Queue",
        max_items=MAX_ITEMS,
        max_length=MAX_VALUE_LENGTH,
    )


def deque():
    return render_template(
        "deque.html",
        title="Deque",
        max_items=MAX_ITEMS,
        max_length=MAX_VALUE_LENGTH,
    )


def sorting():
    return render_template(
        "sorting.html",
        title="Sorting",
        algorithms=SORTING_INFO,
        references=REFERENCES,
    )


def structures_api(kind):
    if request.content_length and request.content_length > 16000:
        return jsonify(error="This request is too large for the demo."), 400
    try:
        return jsonify(structure_action(kind, request.get_json(silent=True)))
    except ValueError as exception:
        return jsonify(error=str(exception)), 400


def sorting_api():
    if request.content_length and request.content_length > 16000:
        return jsonify(error="This request is too large for the demo."), 400
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error="Enter numbers and choose an algorithm."), 400
    try:
        return jsonify(
            sort_numbers(
                payload.get("numbers"),
                payload.get("algorithm", "bubble"),
                payload.get("order", "asc"),
            )
        )
    except ValueError as exception:
        return jsonify(error=str(exception)), 400


def uppercase():
    return render_template("uppercase.html")


def triangle():
    return render_template("triangle.html")


def circle():
    return render_template("circle.html")


def linked_list():
    return render_template("linked-list.html")


def infix_postfix():
    expression, postfix, nodes, steps, error = "", "", [], [], ""
    if request.method == "POST":
        expression = request.form.get("expression", "")
        try:
            postfix, nodes, steps = infix_to_postfix(expression)
        except ValueError as exception:
            error = str(exception)
    return render_template(
        "infix-postfix.html",
        expression=expression,
        postfix=postfix,
        nodes=nodes,
        steps=steps,
        error=error,
    )


def register_works_routes(app):
    # Explicit endpoint names preserve the existing url_for(...) calls in templates.
    app.add_url_rule("/works", endpoint="works", view_func=works)
    app.add_url_rule("/queue", endpoint="queue", view_func=queue)
    app.add_url_rule("/deque", endpoint="deque", view_func=deque)
    app.add_url_rule("/sorting", endpoint="sorting", view_func=sorting)
    app.add_url_rule(
        "/api/structures/<kind>",
        endpoint="structures_api",
        view_func=structures_api,
        methods=["POST"],
    )
    app.add_url_rule(
        "/api/sorting",
        endpoint="sorting_api",
        view_func=sorting_api,
        methods=["POST"],
    )
    app.add_url_rule("/uppercase", endpoint="uppercase", view_func=uppercase)
    app.add_url_rule("/triangle", endpoint="triangle", view_func=triangle)
    app.add_url_rule("/circle", endpoint="circle", view_func=circle)
    app.add_url_rule(
        "/linked-list",
        endpoint="linked_list",
        view_func=linked_list,
    )
    app.add_url_rule(
        "/infix-postfix",
        endpoint="infix_postfix",
        view_func=infix_postfix,
        methods=["GET", "POST"],
    )
