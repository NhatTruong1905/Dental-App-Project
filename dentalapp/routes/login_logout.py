from flask import Blueprint, render_template, request, redirect
from dentalapp.dao.users import auth_user
from flask_login import login_user, logout_user

home_bp = Blueprint('home', __name__)


@home_bp.route('/login')
def login_view():
    return render_template('login.html')


@home_bp.route('/logout')
def logout_process():
    logout_user()
    return redirect('/login')


@home_bp.route('/login', methods=['POST'])
def login_process():
    username = request.form.get('username')
    password = request.form.get('password')
    user = auth_user(username, password)
    if user:
        login_user(user)

    next = request.args.get('next')
    return redirect(next if next else '/')
