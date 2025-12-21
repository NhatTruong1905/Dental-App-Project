from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_babel import Babel
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)

app.secret_key = "!@#$%jasbej%$^(+eiwqbacjfas12399HBAS59^##GSDFG%%jjs;zs4$$"
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:root%40123@localhost/dentaldb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)

admin = Admin(app=app, name="QUẢN TRỊ HỆ THỐNG NHA KHOA")

login = LoginManager(app=app)

babel = Babel(app, locale_selector=lambda: request.accept_languages.best_match(['vi', 'en']))

cloudinary.config(
    cloud_name='dt1pa28g2',
    api_key='824465552867193',
    api_secret='A9MAKfzfQok2sZCjtIuhsDBTzis'
)