from decimal import Decimal
from flask_login import current_user
import requests
from flask import Blueprint, jsonify, flash, url_for, redirect
import os
from dotenv import load_dotenv

from models import Sms, db
from monnify import purchase

load_dotenv()

api_key = os.getenv('SMS_API_KEY')

sms = Blueprint('sms', __name__)

def get_countries():
    url = "https://api.sms-man.com/control/countries?token="
    response = requests.get(url+api_key)

    result = response.json()
    try:
        if not result["success"]:
            flash("An error occured: ", result["error_code"])
            return jsonify(result)
    except:
        return jsonify({
            "success": True,
            "countries": list(result.values())
        })


def get_services():
    url = "https://api.sms-man.com/control/applications?token="
    response = requests.get(url+api_key)
    
    result = response.json()

    try:
        if not result["success"]:
            flash("Error occured ", result["error_code"])
            return jsonify(result)
    except:
        
        return jsonify({
            "success": True,
            "services": list(result.values())
        })

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
        data = filter_data(list(result.values()), application_id, country_id)
        
        return jsonify({
            "success": True,
            "data": data
        })

def filter_data(data, application_id, country_id):
    return [
        item for item in data
        if item['application_id'] == application_id and item['country_id'] == country_id
    ][0] if data != [] else None

@sms.route("/request-number/<application_id>/<country_id>/<amount>")
def request_number(application_id, country_id, amount):
    url = "https://api.sms-man.com/control/get-number?token="+api_key+"&country_id="+country_id+"&application_id="+application_id+"&ref=F8uWN6J3MZfV"
    response = requests.get(url)
    result = response.json()
    try:
        if not result["success"]:
            return jsonify(result)
    except:
        trans = purchase(current_user.email, amount)
        response = trans.get_json()
        if response['status']=="success":
            request_id = result['request_id']
            country_id = result['country_id']
            application_id = result['application_id']
            amount = amount
            number = result['number']

            
            new_sms = Sms(user_id=current_user.id, request_id=request_id,
                        country_id=country_id, application_id=application_id,
                        amount=Decimal(amount), number=number)
            db.session.add(new_sms)
            db.session.commit()
           
            return jsonify({
                "success": True,
                "data": result
            })
        else:
            reject_number(result['request_id'])
           
            return jsonify({
                "success": False,
                "data": response
            })

def reject_number(request_id):
    url = "https://api.sms-man.com/control/set-status?token="+api_key+"&request_id="+request_id+"&status=reject"
    response = requests.get(url)
    result = response.json()

    if result['success']:
        return jsonify(result)

@sms.route("/receive-sms/<request_id>")
def get_sms(request_id):
    url ="https://api.sms-man.com/control/get-sms?token="+api_key+"&request_id="+request_id 
    response = requests.get(url)
    result = response.json()
    sms_code = ''
    try:
        if result['error_code']:
            return jsonify(result)
    except:
        request_id = result['request_id']
        sms_code = result['sms_code']
        initial_sms = Sms.query.filter_by(request_id=request_id).first()
        if initial_sms:
            initial_sms.sms_code = sms_code
            db.session.commit()
    return jsonify(result)
