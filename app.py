from flask import Flask, render_template

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

# Simulan ang local website sa http://127.0.0.1:8000/.
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
