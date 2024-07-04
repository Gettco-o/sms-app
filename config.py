import os
SECRET_KEY = os.urandom(32)

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

MAIL_SERVER ='sandbox.smtp.mailtrap.io'
MAIL_PORT = 2525
MAIL_USERNAME = 'e29f3da09656bd'
MAIL_PASSWORD = '5564c6f6da2cb0'
MAIL_USE_TLS = True
MAIL_USE_SSL = False


SMS_API_KEY = "NPgHgcgx6iO7_FXXGAbknuLwFruvxTtW"

SQLALCHEMY_DATABASE_URI = 'postgresql://smsuser:smsapp@localhost:5432/smsapp'

SQLALCHEMY_TRACK_MODIFICATIONS = False
