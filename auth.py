from flask import Blueprint, request, flash, redirect, url_for, render_template
from flask_login import login_user, logout_user, current_user
import sys
from werkzeug.security import generate_password_hash, check_password_hash

from flask_mail import Mail, Message

from itsdangerous import SignatureExpired, URLSafeTimedSerializer


from models import User, db

import os
from dotenv import load_dotenv


from monnify import create_wallet

load_dotenv()

auth = Blueprint('auth', __name__)

secret_key = os.getenv('SECRET_KEY')


mail = Mail()

s = URLSafeTimedSerializer(secret_key)

@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route("/login", methods=['POST'])
def login_post():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember = True if request.form.get('remember') else False
        try:
            user = User.query.filter_by(email=email).first()
        
            if not user or not check_password_hash(user.password, password):
                flash("Incorrect login details", "danger")
                return redirect(url_for('login'))
            if user.email_verified:
                print("Remebr is ", remember)
                login_user(user, remember=remember)
                flash('Logged in successfully!', 'success')
                return redirect(url_for('dashboard'))
                
            else:
                flash('Please verify your email before logging in.', 'danger')
        except:
            print(sys.exc_info())
    return render_template('login.html') 

        

@auth.route("/signup")
def signup():
    return render_template("signup.html")

@auth.route("/signup", methods=['POST'])
def signup_post():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']


        try:
            user = User.query.filter_by(email=email).first()
            if user:
                flash("email address already registered", 'danger')
                return redirect(url_for('auth.login'))
            
            new_user = User(fullname=fullname, email=email, password=generate_password_hash(password))
            
            db.session.add(new_user)
            db.session.commit()
            print("new_user", new_user)
            flash("User sign up succesful", "success")

            token = s.dumps(email, salt='email-confirm')
            link = url_for('auth.verify_email', token=token, _external=True)
            print("token, link ", token, link)
            msg = Message(subject='Email Verification', sender='codeplugng@gmail.com', recipients=[email])
            msg.body = f'Your link is {link}'
            mail.send(msg)
            print(msg)
            flash('A confirmation email has been sent via email.', 'success')
            
            return redirect(url_for('auth.login'))
        except:
            flash("error occured", 'danger')
            print(sys.exc_info())
            db.session.rollback()
    return render_template('signup.html')


@auth.route('/verify_email/<token>')
def verify_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        flash('The confirmation link has expired.', 'danger')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email).first_or_404()
    if user.email_verified:
        flash('Account already verified. Please login.', 'success')
    else:
        user.email_verified = True
        db.session.commit()
        create_wallet(str(user.id), user.fullname, user.email)
        flash('Your account has been verified!', 'success')
    return redirect(url_for('auth.login'))

@auth.route("/change-password", methods=['POST'])
def change_password():
    if request.method == 'POST':
        current_password = request.form['currentpassword']
        new_password = request.form['newpassword']
        user = User.query.filter_by(email=current_user.email).first_or_404()

        try:
            if check_password_hash(user.password, current_password):
                user.password = generate_password_hash(new_password)
                db.session.commit()
                logout_user()
                flash("Please sign in with new password", "success")
                return redirect(url_for('auth.login'))
            else:
                flash("Incorrect Password", "danger")
        except:
            db.session.rollback()
    return

@auth.route("/forgot-password", methods=['POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']

        try:
            user = User.query.filter_by(email=email).first()
            if not user:
                flash("email address is not registered", 'danger')
                return redirect(url_for('auth.signup'))

            token = s.dumps(email, salt='password-reset')
            link = url_for('auth.reset_password', token=token, _external=True)
            print("token, link ", token, link)
            msg = Message(subject='Password Reset', sender=os.getenv('MAIL_USERNAME'), recipients=[email])
            msg.body = f'Your link is {link}'
            mail.send(msg)
            print(msg)
            flash('A password reset link has been sent via email.', 'success')
            
            return redirect(url_for('auth.login'))
        except:
            flash("error occured", 'danger')
            print(sys.exc_info())
            db.session.rollback()
    return render_template('login.html')
    
@auth.route("/reset-password/<token>")
def reset_password(token):
    try:
        email = s.loads(token, salt='password-reset', max_age=3600)
    except SignatureExpired:
        flash('The password reset link has expired.', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('reset-password.html', email=email)

@auth.route("/reset-password/commit", methods=['POST'])
def commit_password():
    if request.method=='POST':
        email = request.form['email']
        password = request.form['newrspassword']
        user = User.query.filter_by(email=email).first_or_404()
        try:
            user.password = generate_password_hash(password)
            db.session.commit()
            flash('Your password has been changed!', 'success')
        except:
            flash('An error occured')
            db.session.rollback()
    return redirect(url_for('auth.login'))





@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
