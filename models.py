from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import uuid
from decimal import Decimal

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fullname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    email_verified = db.Column(db.Boolean, default=False)
    sms = db.relationship('Sms', backref='user', lazy=True)


    
class Wallet(db.Model):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_email = db.Column(db.String(50), unique=True, nullable=False)
    balance = db.Column(db.Numeric(10, 2), default=0)


class Transaction(db.Model):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_email = db.Column(db.String(50), unique=False, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    transaction_reference = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)


class Sms(db.Model):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey(
        'user.id'
    ), nullable=False)
    request_id = db.Column(db.Integer, nullable=False)
    country_id = db.Column(db.Integer, nullable=False)
    application_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False, default=Decimal(75))    
    number = db.Column(db.String(50), nullable=False)
    sms_code = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    