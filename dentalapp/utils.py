import hashlib
from functools import wraps
from flask_login import current_user


def hash_password(password):
    return hashlib.md5(password.strip().encode('utf-8')).hexdigest()

def is_image(file):
    return file.lower().endswith(('.jpg', '.jpeg', '.png'))

def permission(user_role=None):
    '''
    this decorator requires user login. If this is the default setting, any user can access it.
    Otherwise only users in the list can access it
    user_role=None default
    user_role = [UserRole.ADMIN, UserRole.USER] ADMIN and USER can access.

    :param user_role: list, tuple
    '''
    def decorated_login_required(function):
        @wraps(function)
        def decorated_function(*args, **kwargs):
            if current_user.is_authenticated and user_role is None:
                return function(*args, **kwargs)
            elif current_user.is_authenticated and user_role is not None and current_user.user_role in user_role:
                return function(*args, **kwargs)
            return "You can't access this page!"
        return decorated_function
    return decorated_login_required


