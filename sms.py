import requests
from config import SMS_API_KEY
from flask import Blueprint, jsonify, flash
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('SMS_API_KEY')

sms = Blueprint('sms', __name__)


def check_balance():
    url = url = "https://api.sms-man.com/control/get-balance?token="
    response = requests.get(url+api_key)
    result = response.json()

    try:
        if not result["success"]:
            print("error occured", result)
            return jsonify(result)
    except:
        print(result)

@sms.route("/countries")
def get_countries():
    url = "https://api.sms-man.com/control/countries?token="
    response = requests.get(url+api_key)

    result = response.json()
    try:
        if not result["success"]:
            print("error occured", result)
            flash("An error occured: ", result["error_code"])
            return jsonify(result)
    except:
        #print(list(result.values()))

        return jsonify({
            "success": True,
            "countries": list(result.values())
        })


@sms.route("/services")
def get_services():
    url = "https://api.sms-man.com/control/applications?token="
    response = requests.get(url+api_key)
    print(response.json)

    result = response.json()

    try:
        if not result["success"]:
            flash("Error occured ", result["error_code"])
            return jsonify(result)
    except:
        #print(list(result.values()))
        
        return jsonify({
            "success": True,
            "services": list(result.values())
        })

def get_limits(application_id, country_id):
    url = "https://api.sms-man.com/control/limits?token="+api_key+"&country_id="+country_id+"&application_id="+application_id
    response = requests.get(url)

    result = response.json()
    try:
        if not result["success"]:
            print("Error ", result)
    except:
        print(list(result.values())[0])

@sms.route("/get-prices/<application_id>/<country_id>")
def get_prices(application_id, country_id):
    url = "https://api.sms-man.com/control/get-prices?token="+api_key+"&country_id="+country_id
    response = requests.get(url)

    result = response.json()
    try:
        if not result["success"]:
            flash("Error occured ", result["error_code"])
            return jsonify(result)
    except:
        #print(list(result.values()))
        data = filter_data(list(result.values()), application_id, country_id)
        print("data is ", data)

        return jsonify({
            "success": True,
            "data": data
        })

def filter_data(data, application_id, country_id):
    return [
        item for item in data
        if item['application_id'] == application_id and item['country_id'] == country_id
    ][0]
    


#check_balance() # single dict, balance, hold, channels
#get_countries()  #list of dicts, id, title, code
#get_services() # list of dicts, id, title, code
#get_limits("2", "3")  #single dict, application_id, country_id, numbers
#get_prices("2", "3")  #single dict, cost, count, application_id, country_id
