import json
from flask import Flask, render_template, abort, request
from mock_data import mock_data
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# put dict here
me = {
    "name": "Kenny",
    "last": "Cruz",
    "email": "kennyc@gmail.com",
    "age": 25,
    "hobbies": [],
    "address": {
        "street": "sesame",
        "number": 123
    }
}


@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return f"{me['name']} {me['last']} {'Age: '} {me['age']}"


@app.route("/about/email")
def email():
    return f"{me['email']}"


@app.route("/about/address")
def address():
    address = me["address"]
    print(type(address))
    return f"{address['number']} {address['street']}"


@app.route("/api/catalog", methods=["GET"])
def get_catalog():
    print(request.headers)
    return json.dumps(mock_data)


@app.route("/api/catalog", methods=["POST"])
def save_product():
    product = request.get_json()

    if not "price" in product or product["price"] <= 0:
        abort(400, "Price is required and should be greater than 0")

    if not "title" in product or len(product["title"]) < 5:
        abort(400, "Title is required and must be at least 5 characters long")

    mock_data.append(product)
    product["_id"] = len(product["title"])
    return json.dumps(mock_data)


@app.route("/api/catalog/<cat>")
def get_category(cat):
    found = False
    categories = []
    for prod in mock_data:
        if prod["category"].lower() == cat.lower():
            found = True
            categories.append(prod)
    if found:
        return json.dumps(categories)
    elif not found:
        abort(404)


@app.route("/api/categories")
def get_categories():
    categories = []
    for product in mock_data:
        category = product["category"]
        if category not in categories:
            categories.append(category)

    return json.dumps(categories)


@app.route("/api/product/<id>")
def get_id(id):
    found = False
    for prod in mock_data:
        if prod["_id"] == id:
            found = True
            return json.dumps(prod)
    if not found:
        abort(404)


@app.route("/api/product/cheapest")
def get_cheapest():
    cheap = mock_data[0]
    for prod in mock_data:
        if prod["price"] < cheap["price"]:
            cheap = prod
    return json.dumps(cheap)


app.run(debug=True)
