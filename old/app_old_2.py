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





@app.route('/')
def index():
    return render_template('index.html')


######################################


# get all stores and their items
@app.get("/store/")
def get_stores():
    return {"stores": list(stores.values())}


# create store
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


# get store
@app.get("/store/<string:store_id>/")
def get_store(store_id):
    try:
        return stores[store_id]
    except Exception:
        abort(404, message="Store not found.")


# delete store
@app.delete("/store/<string:store_id>/")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted."}
    except KeyError:
        abort(404, message="Store not found.")





######################################

# get all items
@app.get("/item/")
def get_items():
    return {"items": list(items.values())}
        
        
# get item
@app.get("/item/<string:item_id>/")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found.")
        

# create item
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



# delete item
@app.delete("/item/<string:item_id>/")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted."}
    except KeyError:
        abort(404, message="Item not found.")


# update item
@app.put("/item/<string:item_id>/")
def update_item(item_id):
    item_data = request.get_json()

    if "price" not in item_data or "name" not in item_data:
        abort( 400, message="Bad request. Ensure 'price', and 'name' are included in the JSON payload.")
    try:
        item = items[item_id]
        # item |= item_data # support in python 3.9
        item.update(item_data)
        
        return item
    except KeyError:
        abort(404, message="Item not found.")



######################################

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
