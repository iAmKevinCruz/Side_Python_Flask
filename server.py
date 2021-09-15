import json
from flask import Flask, render_template
from mock_data import mock_data
app = Flask(__name__)

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


@app.route("/api/catalog")
def get_catalog():
    return json.dumps(mock_data)


@app.route("/api/categories")
def get_categories():
    categories = []
    for product in mock_data:
        category = product["category"]
        if category not in categories:
            categories.append(category)

    return json.dumps(categories)


app.run(debug=True)
