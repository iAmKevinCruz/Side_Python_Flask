from os import truncate
from mock_data import mock_data


class Dog:
    def __init__(self, name):
        self.name = name


me = {
    "name": "Kevin",
    "last": "Cruz",
    "email": "test@gmail.com",
    "age": 28,
    "hobbies": [],
    "address": {
        "street": "main",
        "number": 42
    }
}


def print_data():
    print(me["name"])
    print(me["name"] + " " + me["last"])

    # create an object of Dog class
    fido = Dog("Fido")
    print(fido.name)

    print(type(me))
    print(type(fido))


# print_data()


def test_list():
    print("Working with lists")
    names = []

    names.append("Kevin")
    names.append("Sergio")
    names.append("Darrow")
    print("---------------------For Loop Example")
    for name in names:
        print("For Loop: " + name)

    print("------------------Sublist")
    # sublist    list[<skip> : <take>]
    print(names[1:])


# test_list()

def product_search():

    print("------------------------------------------")
    print("How would you like to search?")
    print("[1] Search by ID")
    print("[2] Search by Category")
    print("------------------------------------------")

    option = input("Choose: ")

    if option == "1":
        id = input("What ID are you looking for? - ")
        found = False
        for product in mock_data:
            if product["_id"] == id:
                found = True
                print("------------------------------------------")
                print(product)
                print("------------------------------------------")

        if not found:
            print("Error: No product with ID: '" + id + "' found!")
            return None
    elif option == "2":
        category = input("What category are you looking for? - ")
        categories = []
        found = False
        for product in mock_data:
            if product["category"] == category:
                found = True
                categories.append(product)
                print("------------------------------------------")
                print(product)
                print("------------------------------------------")
        if not found:
            print("Error: No product with category: '" + category + "' found!")
            return None


product_search()
