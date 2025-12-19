import re

from dentalapp.models import User
import cloudinary.uploader
from dentalapp import db
from dentalapp.utils import hash_password


def get_current_user(user_id):
    return User.query.get(user_id)

def auth_user(username, password):
    password = hash_password(password)
    return User.query.filter(User.username == username, User.password == password).first()


def add_user(name, phone, username, password, avatar):
    password = hash_password(password)
    user = User(name=name.strip(), phone=phone, username=username.strip(), password=password)
    if avatar:
        res = cloudinary.uploader.upload(avatar)
        user.avatar = res.get("secure_url")
    db.session.add(user)
    db.session.commit()

def change_password(user, new_password):
    user.password = hash_password(new_password)
    db.session.commit()


def validate_username(username):
    return not User.query.filter(User.username==username).first()


def validate_phone(phone):
    return bool(re.match(r"^(01|02|03|04|05|06|07|08|09)\d{8}$", phone))


def validate_password(pwd, confirm):
    return pwd == confirm
