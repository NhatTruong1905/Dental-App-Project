from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_babel import Babel
from flask_login import LoginManager
import cloudinary
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['PAGE_SIZE'] = 6

db = SQLAlchemy(app=app)

admin = Admin(app=app, name="QUẢN TRỊ HỆ THỐNG NHA KHOA")

login = LoginManager(app=app)

babel = Babel(app, locale_selector=lambda: request.accept_languages.best_match(['vi', 'en']))

cloudinary.config(
    cloud_name='dt1pa28g2',
    api_key='824465552867193',
    api_secret='A9MAKfzfQok2sZCjtIuhsDBTzis'
)
