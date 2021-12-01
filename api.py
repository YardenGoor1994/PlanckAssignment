import flask
from flask import request, jsonify
import requests as req
import json
import schedule
import time
from enum import Enum

app = flask.Flask(__name__)
app.config["DEBUG"] = True

class categories_names(Enum):
    PIZZA = 'Pizzas'
    DRINKS = 'Drinks'
    DESSERT = 'Desserts'

class properties(Enum):
    DATA = 'Data'
    CATEGORIES_LIST = 'categoriesList'
    CATEGORY_NAME = 'categoryName'
    DISH_LIST = 'dishList'
    DISH_ID = 'dishId'
    DISH_NAME = 'dishName'
    DISH_DESCRIPTION = 'dishDescription'
    DISH_PRICE = "dishPrice"

menu = None


def refresh_data():
    global menu
    menu = json.loads(req.get(
        "https://www.10bis.co.il/NextApi/GetRestaurantMenu?culture=en&uiCulture=en&restaurantId=19156&deliveryMethod=pickup").text)


def get_category_item_list(category):
    categories = menu[properties.DATA.value][properties.CATEGORIES_LIST.value]
    item_list = []
    for c in categories:
        if c[properties.CATEGORY_NAME.value] == category:
            item_list = c[properties.DISH_LIST.value]
            break
    return item_list

def get_filtered_items(items,id_filter = None):
    return_value = []
    for item in items:
        if id_filter is None or int(item[properties.DISH_ID.value]) == int(id_filter):
            return_value.append({properties.DISH_ID.value: item[properties.DISH_ID.value],
                                 properties.DISH_NAME.value: item[properties.DISH_NAME.value],
                                 properties.DISH_DESCRIPTION.value: item[properties.DISH_DESCRIPTION.value],
                                 properties.DISH_PRICE.value: item[properties.DISH_PRICE.value]})
            if id_filter is not None:
                break
    if len(return_value)==0:
        return_value.append("No items found with this id")
    return return_value

def sum_price_of_items_in_category(category,items_ids):
    item_list = get_category_item_list(category)
    total_price=0
    for item in items_ids:
        total_price += get_filtered_items(item_list, item)[0][properties.DISH_PRICE.value]
    return total_price


@app.route('/', methods=['GET'])
def home():
    return jsonify(menu)

@app.route('/drinks', methods=['GET'])
def all_drinks_api():
    drinks = get_category_item_list(categories_names.DRINKS.value)
    return_value = get_filtered_items(drinks)
    return jsonify(return_value)

@app.route('/drink/<drink_id>', methods=['GET'])
def drink_api(drink_id):
    drinks = get_category_item_list(categories_names.DRINKS.value)
    return_value = get_filtered_items(drinks,drink_id)
    return jsonify(return_value[0])

@app.route('/pizzas', methods=['GET'])
def all_pizzas_api():
    pizzas = get_category_item_list(categories_names.PIZZA.value)
    return_value = get_filtered_items(pizzas)
    return jsonify(return_value)

@app.route('/pizza/<pizza_id>', methods=['GET'])
def pizza_api(pizza_id):
    pizzas = get_category_item_list(categories_names.PIZZA.value)
    return_value = get_filtered_items(pizzas,pizza_id)
    return jsonify(return_value[0])

@app.route('/desserts', methods=['GET'])
def all_desserts_api():
    desserts = get_category_item_list(categories_names.DESSERT.value)
    return_value = get_filtered_items(desserts)
    return jsonify(return_value)

@app.route('/dessert/<dessert_id>', methods=['GET'])
def dessert_api(dessert_id):
    desserts = get_category_item_list(categories_names.DESSERT.value)
    return_value = get_filtered_items(desserts,dessert_id)
    return jsonify(return_value[0])

@app.route('/order', methods=['GET','POST'])
def order_price_api():
    content = request.get_json(force=True)
    total_price = 0
    for key,item_ids in content.items():
        for category in categories_names:
            if key == category.value.lower():
                total_price += sum_price_of_items_in_category(category.value, item_ids)
                break
    return jsonify({"price": total_price})

refresh_data()
schedule.every().day.at("00:00").do(refresh_data)
app.run()
while True:
    schedule.run_pending()
    time.sleep(1)