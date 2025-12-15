from dentalapp.models import User


def get_current_user(user_id):
    return User.query.get(user_id)