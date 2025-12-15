import hashlib

from dentalapp.models import User


def get_current_user(user_id):
    return User.query.get(user_id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username == username, User.password == password).first()
