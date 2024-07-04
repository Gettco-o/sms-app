from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import uuid

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fullname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    email_verified = db.Column(db.Boolean, default=False)
    wallet = db.relationship('Wallet', backref='user', lazy=True)
    transaction = db.relationship('Transaction', backref='user', lazy=True)


    
class Wallet(db.Model):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_reference = db.Column(db.UUID(as_uuid=True), db.ForeignKey(
        'user.id'
    ), nullable=False)
    balance = db.Column(db.Numeric(10, 2), default=0)


class Transaction(db.Model):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True)
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey(
        'user.id'
    ), nullable=False)
    account_reference = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())