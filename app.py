from flask import Flask, render_template, url_for
from models import db, User, Wallet
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_login import login_required, current_user
from auth import mail
from flask_cors import CORS
import os
from dotenv import load_dotenv

from monnify import get_wallet

load_dotenv()

app = Flask(__name__, template_folder='./templates/', static_folder='./static/')

#app.config.from_object('config')

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY']=os.getenv('SECRET_KEY')
app.config['DEBUG'] = os.getenv('DEBUG').lower() in ['true', '1', 't', 'y', 'yes']

app.config['SQLALCHEMY_DATABASE_URI']=os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')

app.config['MAIL_SERVER']=os.getenv('MAIL_SERVER')
app.config['MAIL_PORT']=int(os.getenv('MAIL_PORT'))
app.config['MAIL_USERNAME']=os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD']=os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS').lower() in ['true', '1', 't', 'y', 'yes']
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL').lower() in ['true', '1', 't', 'y', 'yes']


db.init_app(app)

mail.init_app(app)

CORS(app)


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

migrate = Migrate(app, db)

from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from sms import get_countries, get_services, sms as sms_blueprint
app.register_blueprint(sms_blueprint)

from monnify import monnify as monnify_blueprint
app.register_blueprint(monnify_blueprint)

@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    return response


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/dashboard")
@login_required
def dashboard():
    wallet = Wallet.query.filter_by(user_email=current_user.email).first()
    balance = wallet.balance if wallet else 0
    balance = "{:,}".format(balance)
    return render_template('dashboard.html', user = current_user, balance=balance)

@app.route("/profile")
@login_required
def profile():
    return render_template('profile.html', user = current_user)

@app.route("/receive-sms")
@login_required
def receive_sms():
    countries = get_countries()
    services = get_services()
    data1 = countries.get_json()
    data2 = services.get_json()
      

    return render_template('receive_sms.html', countries = data1["countries"], services=data2["services"])

@app.route("/deposit")
@login_required
def deposit():
    account = get_wallet(current_user.id)
    account = account.get_json()
    return render_template('deposit.html', account=account)


# run the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)