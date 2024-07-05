import base64
from decimal import Decimal
import requests
import time
from flask import Blueprint, jsonify, flash, request
from models import Wallet, Transaction, db
import hashlib
import hmac
import os
from dotenv import load_dotenv

load_dotenv()

monnify = Blueprint('monnify', __name__)

api_key = os.getenv('MONNIFY_API_KEY')
secret_key = os.getenv('MONNIFY_SECRET_KEY')

credentials = f"{api_key}:{secret_key}"

encoded_credentials = base64.b64encode(credentials.encode()).decode()

headers = {
    'Authorization': f'Basic {encoded_credentials}'
}

auth_url = os.getenv('MONNIFY_AUTH_URL')

base_url = os.getenv('MONNIFY_BASE_URL')

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

@monnify.route('/webhook', methods=['POST'])
def webhook():
    print("launched")
    ensure_valid_token()

    monnify_signature = request.headers.get('monnify-signature')
    if not monnify_signature:
        return jsonify({"status": "error", "message": "Missing monnify-signature header"}), 400

    # Get the raw request body
    request_body = request.get_data(as_text=True)

    # Compute the hash
    computed_hash = hmac.new(
        secret_key.encode(), 
        request_body.encode(), 
        hashlib.sha512
    ).hexdigest()

    # Compare the computed hash with the 'monnify-signature'
    if computed_hash != monnify_signature:
        return jsonify({"status": "error", "message": "Invalid signature"}), 400

    #data = request.get_json()
    data = request.json
    if data['eventType'] == 'SUCCESSFUL_TRANSACTION':
        #account_reference = data['eventData']['accountReference']
        user_email = data['eventData']['customer']['email']
        created_at = data['eventData']['paidOn']   
        amount_paid = Decimal(data['eventData']['amountPaid'])
        transaction_reference = data['eventData']['transactionReference']
        status = data['eventType']

        wallet = Wallet.query.filter_by(user_email=user_email).first()
        if wallet:
            wallet.balance += amount_paid
        else:
            wallet = Wallet(user_email=user_email, balance=amount_paid)
            db.session.add(wallet)

        initTrans = Transaction.query.filter_by(transaction_reference=transaction_reference).first()
        if initTrans:
            return jsonify({"status": "error", "message": "Transaction already exists"}), 400
        
        transaction = Transaction(user_email=user_email, amount=amount_paid, created_at=created_at, 
                                  transaction_reference=transaction_reference, 
                                  transaction_type='deposit', status=status)
        db.session.add(transaction)
        db.session.commit()

        print(f"Updated wallet for {user_email}: {wallet.balance}")
    
    return jsonify({"status": "success"}), 200

@monnify.route('/purchase', methods=['POST'])
def purchase():
    data = request.json
    user_email = data['eventData']['customer']['email']
    purchase_amount = Decimal(data['purchase_amount'])

    wallet = Wallet.query.filter_by(user_email=user_email).first()
    if not wallet or wallet.balance < purchase_amount:
        return jsonify({"status": "error", "message": "Insufficient funds"}), 400

    wallet.balance -= purchase_amount
    transaction = Transaction(user_email=user_email, amount=purchase_amount, transaction_type='purchase')
    db.session.add(transaction)
    db.session.commit()

    return jsonify({"status": "success", "remaining_balance": wallet.balance}), 200
