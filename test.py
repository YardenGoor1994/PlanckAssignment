import requests
import json
URL = 'http://127.0.0.1:5000/'


def api_test_status():
    response = requests.get(URL)
    print ("status test - does the API connect: " + ("Success" if response.status_code==200 else "fail"))

def api_test_response_format():
    response = requests.get(URL)
    print ("format test - is the response in JSON format: " + ("Success" if response.headers['content-type'] == "application/json" else "fail"))

def api_test_drinks():
    response = requests.get(URL + "/drinks")
    print("value test - is the drinks API returning correct values: " + (
        "Success" if len(response.json()) == 8 else "fail"))
    print(response.json())

def api_test_drink_found():
    response = requests.get(URL + "/drink/2055846")
    print("value test - drink/id API returning values when there should be: " + (
        "Success" if len(response.json()) == 4 else "fail"))
    print(response.json())

def api_test_drink_not_found():
    response = requests.get(URL + "/drink/123")
    print("value test - drink/id API not returning values when there shouldnt be: " + (
        "Success" if response.json() == "No items found with this id" else "fail"))
    print(response.json())
def api_test_put_order():
    json_data = {"drinks":[2055846,2055838],"pizzas": [2055830],"desserts": [2055837]}
    response = requests.post(URL+"/order",json = json_data)
    print("value test - order API returnes correct price: " + (
        "Success" if response.json()["price"] == 105 else "fail"))
    print(response.json())

if __name__ == "__main__":
    api_test_status()
    api_test_response_format()
    api_test_drinks()
    api_test_drink_found()
    api_test_drink_not_found()
    api_test_put_order()