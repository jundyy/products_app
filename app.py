import csv
import os

headers = ["id", "name", "aisle", "department", "price"]
user_input_headers = [header for header in headers if header != "id"]


def menu(username, products_count):
    # this is a multi-line string, also using preceding `f` for string interpolation

    menu = f"""
    -----------------------------------
    INVENTORY MANAGEMENT APPLICATION
    -----------------------------------
    Welcome {username}!
    There are {products_count} products in the database.
        operation | description
        --------- | ------------------
        'List'    | Display a list of product identifiers and names.
        'Show'    | Show information about a product.
        'Create'  | Add a new product.
        'Update'  | Edit an existing product.
        'Destroy' | Delete an existing product. 
        'Menu'    | Show this menu again"""  # end of multi- line string. also using string interpolation

    return menu


def read_products_from_file(filename="products.csv"):
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
    print(f"READING PRODUCTS FROM FILE: '{filepath}'")
    products = []

    with open(filepath, "r") as csv_file:
        reader = csv.DictReader(csv_file)  # assuming your CSV has headers, otherwise... csv.reader(csv_file)
        for row in reader:
            # print(row["name"], row["price"])
            products.append(dict(row))

    return products


def write_products_to_file(filename="products.csv", products=[]):
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
    # print(f"OVERWRITING CONTENTS OF FILE: '{filepath}' \n ... WITH {len(products)} PRODUCTS")

    with open(filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["id", "name", "aisle", "department", "price"])
        writer.writeheader()  # uses fieldnames set above

        for p in products:
            writer.writerow(p)


def reset_products_file(filename="products.csv", from_filename="products_default.csv"):
    print("RESETTING DEFAULTS")
    products = read_products_from_file(from_filename)
    write_products_to_file(filename, products)


def run():
    # First, read products from file...
    products = read_products_from_file()
    products_count = len(products)

    username = "Human Person"

    # Then, prompt the user to select an operation...
    print(menu(username, products_count))

    task = input("Please enter your desired operation: ")

    while True:
        if task not in ("List", "Show", "Create", "Destroy", "Update", "Destroy"):
            task = input("Please enter a valid operation: ")
            continue
        else:
            break

    while True:

        # Then, handle selected operation: "List", "Show", "Create", "Update", "Destroy" or "Reset"...
        if task == "List":

            for p in products:
                print(" + ", p["id"], p["name"])

        elif task == "Show":

            item = int(input("Please enter an item ID to show: "))
            matching_products = [p for p in products if int(item) == int(p["id"])]
            matching_product = matching_products[0]
            print(matching_product)

        elif task == "Create":
            all_ids = [int(p["id"]) for p in products]
            new_id = max(all_ids) + 1
            new_product = {
                "id": new_id,
                "name": "New Product",
                "aisle": "new aisle",
                "department": "new department",
                "price": "price"
            }

            p_name = input("Please enter the new products name: ")
            p_aisle = input("Please enter the new products aisle: ")
            p_department = input("Please enter the new products department: ")
            p_price = input("Please enter the new products price: ")

            new_product["name"] = p_name
            new_product["aisle"] = p_aisle
            new_product["department"] = p_department
            new_product["price"] = float(p_price)

            products.append(new_product)
            products_count = len(products)

        elif task == "Update":

            for p in products:
                print(" + ", p["id"], p["name"])

            item = int(input("Please enter an item ID to update: "))
            matching_products = [p for p in products if int(item) == int(p["id"])]
            product = matching_products[0]

            print(product)

            if product:
                print("Please provide the products information")
                for header in user_input_headers:
                    product[header] = input("Change '{0}' from '{1}' to: ".format(header, product[header]))
                print("Updating product: ", product)
            else:
                print("Product could not be found with ID", product)
            # Source: Professor Rossetti

        elif task == "Destroy":

            item = int(input("Please enter an item ID to delete: "))
            matching_products = [p for p in products if int(item) == int(p["id"])]
            matching_product = matching_products[0]
            print("this will be deleted: ", matching_product)
            del products[products.index(matching_product)]

        elif task == "Menu":

            menu(username, products_count)

        else:
            print("error")

        task = input("Please enter another operation or enter Finish to commit changes: ")

        if task == "Finish":
            break
        else:
            continue

    # Finally, save products to file so they persist after script is done...
    write_products_to_file(products=products)


# only prompt the user for input if this script is run from the command-line
# this allows us to import and test this application's component functions
if __name__ == "__main__":
    run()


