from flask import Blueprint
from dentalapp import login
from flask import render_template
from dentalapp.dao.users import get_current_user

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def home():
    return render_template("index.html")


@login.user_loader
def load_user(user_id):
    return get_current_user(user_id)
