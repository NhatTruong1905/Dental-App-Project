import hashlib
from functools import wraps
from flask_login import current_user
from flask import redirect, abort


def hash_password(password):
    return hashlib.md5(password.strip().encode('utf-8')).hexdigest()

def is_image(file):
    return file.lower().endswith(('.jpg', '.jpeg', '.png'))


def permission(allow=None):
    def decorator(function):
        @wraps(function)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect("/login")

            if allow is None:
                return function(*args, **kwargs)

            if current_user.user_role in allow["roles"]:
                if allow["access"]:
                    return function(*args, **kwargs)
                return abort(403)
            else:
                if not allow["access"]:
                    return function(*args, **kwargs)
                return abort(403)


        return decorated_function
    return decorator
