from flask import Flask, Blueprint, current_app, render_template, request, redirect, url_for
from dotenv import load_dotenv
from os import getenv
import datetime

from db import stores, items
import uuid


from flask_smorest import abort

load_dotenv()
####################################################################

app = Flask(__name__)

# stores = [
#     {
#         "name": "My Store",
#         "items": [
#             {
#                 "name": "Chair",
#                 "price": 15.99
#             }
#         ]
#     }
# ]

# stores = {}
# items = {}




@app.route('/')
def index():
    return render_template('index.html')


# # Retrieve all stores and their items
# @app.get("/store/")
# def get_stores():
#     return {"stores": stores}, 200
# Retrieve all stores and their items
@app.get("/store/")
def get_stores():
    return {"stores": list(stores.values())}



# # Create stores
# @app.post("/store/")
# def create_store():
#     request_data = request.get_json()
#     new_store = {"name": request_data["name"], "items": []}
#     stores.append(new_store)
#     return new_store, 201
# Create stores
@app.post("/store/")
def create_store():
    store_data = request.get_json()
    
    if "name" not in store_data:
        abort( 400, message="Bad request. Ensure 'name' is included in the JSON payload.")
    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(400, message=f"Store already exists.")
    
    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store



# # Create items
# @app.post("/store/<string:name>/item/")
# def create_item(name):
#     request_data = request.get_json()
#     for store in stores:
#         if store["name"] == name:
#             new_item = {"name": request_data["name"], "price": request_data["price"]}
#             store["items"].append(new_item)
#             return new_item
#     return {"message": "Store not found"}, 404
# # Create items
# @app.post("/item")
# def create_item():
#     item_data = request.get_json()
#     if item_data["store_id"] not in stores:
#         # return {"message": "Store not found"}, 404
#         abort(404, message="Store not found.")
#     item_id = uuid.uuid4().hex
#     item = {**item_data, "id": item_id}
#     items[item_id] = item
#     return item
# Create items
@app.post("/item/")
def create_item():
    item_data = request.get_json()
    
    if ("price" not in item_data or "store_id" not in item_data or "name" not in item_data ):
        abort(400, message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.")
    
    for item in items.values():
        if ( item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"] ):
            abort(400, message=f"Item already exists.")

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    return item



# # Get a particular store
# @app.get("/store/<string:name>/")
# def get_store(name):
#     for store in stores:
#         if store["name"] == name:
#             return store
#     return {"message": "Store not found"}, 404
# Get a particular store
@app.get("/store/<string:store_id>/")
def get_store(store_id):
    try:
        return stores[store_id]
    except Exception:
        # return {"message": "Store not found"}, 404
        abort(404, message="Store not found.")



# # Get only items in a store
# @app.get("/store/<string:name>/item/")
# def get_item_in_store(name):
#     for store in stores:
#         if store["name"] == name:
#             return {"items": store["items"]}
#     return {"message": "Store not found"}, 404
# Get only items in a store
@app.get("/item/<string:item_id>/")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        # return {"message": "Item not found"}, 404
        abort(404, message="Item not found.")
        



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
