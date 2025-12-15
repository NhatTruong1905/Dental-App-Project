from flask import Blueprint, render_template, redirect, request
from dentalapp.models import User
import re
from dentalapp.dao import users

register_bp = Blueprint("register", __name__)


@register_bp.route("/register", methods=["GET"])
def register_view():
    return render_template("register.html")

@register_bp.route("/register", methods=["POST"])
def register_process():
    username = request.form.get("username")
    if User.query.filter(User.username==username).first():
        return render_template("register.html", err_msg="Tên đăng nhập đã tồn tại vui lòng chọn tên khác!")

    phone = request.form.get("phone")
    if not bool(re.match(r"^(03|05|07|08|09)\d{8}$", phone)):
        return render_template("register.html", err_msg="Số điện thoạt không hợp lệ vui lòng nhập lại!")

    password = request.form.get("password")
    confirm = request.form.get("confirm")
    if password != confirm:
        return render_template("register.html", err_msg="Mật khẩu không khớp vui lòng nhập lại!")

    name = request.form.get("name")
    avatar = request.files.get("avatar")

    try:
        users.add_user(name=name, phone=phone, username=username, password=password, avatar=avatar)
        return redirect(request.args.get("next"))
    except Exception as ex:
        return render_template("register.html", err_msg=str(ex))