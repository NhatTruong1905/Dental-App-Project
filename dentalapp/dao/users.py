import hashlib
from dentalapp.models import User
import cloudinary.uploader
from dentalapp import db


def get_current_user(user_id):
    return User.query.get(user_id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username == username, User.password == password).first()


def add_user(name, phone, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    user = User(name=name.strip(), phone=phone, username=username.strip(), password=password)
    if avatar:
        res = cloudinary.uploader.upload(avatar)
        user.avatar = res.get("secure_url")
    db.session.add(user)
    db.session.commit()

