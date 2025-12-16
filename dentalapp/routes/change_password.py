from flask import render_template, redirect, Blueprint, request
from flask_login import current_user
from dentalapp.dao.users import hash_password, change_password

change_password_bp = Blueprint('change_password', __name__)


@change_password_bp.route('/change_password', methods=['GET'])
def render_change_pwd():
    if current_user.is_authenticated:
        return render_template('change_password.html')
    else:
        return redirect('/login')

@change_password_bp.route('/change_password', methods=['POST'])
def change_pwd():
    curr_pwd = hash_password(request.form.get('current_password'))
    if curr_pwd != current_user.password:
        return render_template('change_password.html', err_msg="Mật khẩu hiện tại không đúng!")

    new_pwd = request.form.get('new_password')
    confirm_pwd = request.form.get('confirm_password')
    if new_pwd != confirm_pwd:
        return render_template("change_password.html", err_msg="Mật khẩu không khớp vui lòng nhập lại!")

    try:
        change_password(current_user, new_pwd)
        return redirect('/login')
    except Exception as ex:
        return render_template("change_password.html", err_msg=str(ex))
