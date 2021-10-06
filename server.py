import json
from flask import Flask, render_template, abort, request
from mock_data import mock_data
from flask_cors import CORS
from config import db, parse_json

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




# API METHODS

# GETS the catalog/items from the Mongo Database
@app.route("/api/catalog", methods=["GET"])
def get_catalog():
    cursor = db.products.find({})
    catalog = []
    for prod in cursor:
        catalog.append(prod)

    return parse_json(catalog)


@app.route("/api/catalog", methods=["POST"])
def save_product():
    product = request.get_json()

    if not "price" in product or product["price"] <= 0:
        abort(400, "Price is required and should be greater than 0")

    if not "title" in product or len(product["title"]) < 5:
        abort(400, "Title is required and must be at least 5 characters long")

    # mock_data.append(product)
    # product["_id"] = len(product["title"])
    # return json.dumps(mock_data)

    # save product into the DB
    # MongoDB add a _id with a uniqe value
    db.products.insert_one(product)
    return parse_json(product)


@app.route("/api/catalog/<cat>")
def get_category(cat):
    # found = False
    # categories = []
    # for prod in mock_data:
    #     if prod["category"].lower() == cat.lower():
    #         found = True
    #         categories.append(prod)
    # if found:
    #     return json.dumps(categories)
    # elif not found:
    #     abort(404)

    cursor = db.products.find({"category" : cat.lower()})
    products = []
    for prod in cursor:
        products.append(prod)
        
    return parse_json(products)


@app.route("/api/categories")
def get_categories():
    # categories = []
    # for product in mock_data:
    #     category = product["category"]
    #     if category not in categories:
    #         categories.append(category)

    # return json.dumps(categories)

    # return a list with the uniqe categories [string, string]
    cursor = db.products.find({})
    categories = []
    for cat in cursor:
        if cat['category'] not in categories:
            categories.append(cat['category'])
    return parse_json(categories)


@app.route("/api/product/<id>")
def get_id(id):
    # found = False
    # for prod in mock_data:
    #     if prod["_id"] == id:
    #         found = True
    #         return json.dumps(prod)
    # if not found:
    #     abort(404)

    product = db.products.find_one({"_id" : id})
    if not product:
        abort(404)

    return parse_json(product)


@app.route("/api/product/cheapest")
def get_cheapest():
    # cheap = mock_data[0]
    # for prod in mock_data:
    #     if prod["price"] < cheap["price"]:
    #         cheap = prod
    # return json.dumps(cheap)

    cursor = db.products.find()
    cheap = cursor[0]
    for prod in cursor:
        if prod["price"] < cheap["price"]:
            cheap = prod

    return parse_json(cheap)


@app.route("/api/test/loaddata")
def load_data():
    return "Data Already Loaded"

    for prod in mock_data:
        db.products.insert_one(prod)
    return "Data Loaded"



@app.route("/api/couponCode", methods=["POST"])
def save_coupon():
    coupon = request.get_json()
    if not "code" in coupon:
        abort(400, "Title is required")

    if not "discount" in coupon or coupon["discount"] <= 0:
        abort(400, "Discount is required and must be more than 0")
    
    db.couponCodes.insert_one(coupon)
    return parse_json(coupon)

@app.route("/api/couponCode")
def get_coupon():
    cursor = db.couponCodes.find({})
    codes = []
    for code in cursor:
        codes.append(code)
    return parse_json(codes)


app.run(debug=True)
