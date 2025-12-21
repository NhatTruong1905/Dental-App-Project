import hashlib
from functools import wraps
from flask_login import current_user
from flask import redirect


def hash_password(password):
    return hashlib.md5(password.strip().encode('utf-8')).hexdigest()

def is_image(file):
    return file.lower().endswith(('.jpg', '.jpeg', '.png'))

def permission(user_role=None):
    def decorated_login_required(function):
        @wraps(function)
        def decorated_function(*args, **kwargs):
            if current_user.is_authenticated:
                if user_role is None:
                    return function(*args, **kwargs)
                elif user_role is not None and current_user.user_role in user_role:
                    return function(*args, **kwargs)
                else:
                    return "You can't access this page!"
            else:
                return redirect('/login')
        return decorated_function
    return decorated_login_required
