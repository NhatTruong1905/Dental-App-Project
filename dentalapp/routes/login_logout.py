from flask import Blueprint, render_template, request, redirect
from dentalapp.dao.users import auth_user
from flask_login import login_user, logout_user

login_logout_bp = Blueprint('login_logout', __name__)


@login_logout_bp.route('/login')
def render_login():
    return render_template('login.html')


@login_logout_bp.route('/logout')
def logout_process():
    logout_user()
    return redirect('/login')


@login_logout_bp.route('/login', methods=['POST'])
def login_process():
    username = request.form.get('username')
    password = request.form.get('password')
    user = auth_user(username, password)
    login_type = request.form.get('login_type')
    if user:
        login_user(user)

        if user.user_role.value == 4:
            return redirect('/appointment_employees')

        next = request.args.get('next')
        return redirect(next if next else '/')
    elif login_type == "user":
        return render_template('login.html', err_msg="Tên đăng nhập hoặc mật khẩu không chính xác!")
