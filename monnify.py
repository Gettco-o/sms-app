import base64
import requests
import time
from flask import Blueprint, jsonify, flash
from flask_login import login_required, current_user

monnify = Blueprint('monnify', __name__)

base_url = "https://sandbox.monnify.com"
api_key = "MK_TEST_QD3MYQBZST"
secret_key = "UTN0TTBN8C8GF1MVEHTUM3UX6ZPBBBE0"

credentials = f"{api_key}:{secret_key}"

encoded_credentials = base64.b64encode(credentials.encode()).decode()

headers = {
    'Authorization': f'Basic {encoded_credentials}'
}

auth_url = 'https://sandbox.monnify.com/api/v1/auth/login'

base_url = 'https://sandbox.monnify.com'

session = requests.Session()

def get_access_token():
    response = session.post(auth_url, headers=headers, timeout=10)
    if response.status_code == 200:
        data = response.json()["responseBody"]
        access_token = data['accessToken']
        expires_in = data['expiresIn']
        return access_token, expires_in
    else:
        raise Exception("Failed to obtain access token")

access_token, expires_in = get_access_token()
expiry_time = time.time() + expires_in

api_headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

def ensure_valid_token():
    global access_token, expiry_time
    if time.time() >= expiry_time - 60:  # Refresh token 60 seconds before it expires
        access_token, expires_in = get_access_token()
        expiry_time = time.time() + expires_in
        api_headers['Authorization'] = f'Bearer {access_token}'


def create_wallet(user_id, user_name, user_email):
    ensure_valid_token()

    body = {
        "accountReference": user_id,
        "accountName": user_name,
        "currencyCode": "NGN",
        "contractCode": "2031554299",
        "customerEmail": user_email,
        "customerName": "Python Test1",
        "getAllAvailableBanks": True
    }

    response = session.post(f'{base_url}/api/v2/bank-transfer/reserved-accounts', headers=api_headers, json=body, timeout=10)
    return jsonify(response.json())


def get_wallet(account_reference):
    ensure_valid_token()
    response = session.get(f'{base_url}/api/v2/bank-transfer/reserved-accounts/{account_reference}', headers=api_headers, timeout=10)
    res = response.json()
    print(res)
    data = res['responseBody']['accounts']
    return jsonify(data)

def get_balance(account_reference):
    ensure_valid_token()
    response = session.get(f'{base_url}/api/v2/bank-transfer/reserved-accounts/{account_reference}', headers=api_headers, timeout=10)
    res = response.json()
    print(res)
    try:
        data = res['responseBody']['totalAmount']
        return jsonify(data)
    except:
        return jsonify('0')
