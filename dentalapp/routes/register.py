from flask import Blueprint, render_template, redirect, request
from dentalapp.utils import is_image
from dentalapp.dao import users

register_bp = Blueprint("register", __name__)


@register_bp.route("/register", methods=["GET"])
def register_view():
    return render_template("register.html")

@register_bp.route("/register", methods=["POST"])
def register_process():
    username = request.form.get("username")
    if not users.validate_username(username):
        return render_template("register.html", err_msg="Tên đăng nhập đã tồn tại vui lòng chọn tên khác!")

    phone = request.form.get("phone")
    if not users.validate_phone(phone):
        return render_template("register.html", err_msg="Số điện thoạt không hợp lệ vui lòng nhập lại!")

    password = request.form.get("password")
    confirm = request.form.get("confirm")
    if not users.validate_password(password, confirm):
        return render_template("register.html", err_msg="Mật khẩu không khớp vui lòng nhập lại!")

    name = request.form.get("name")
    avatar = request.files.get("avatar")
    if not is_image(avatar.filename):
        return render_template("register.html", err_msg="File không hợp lệ!")

    try:
        users.add_user(name=name, phone=phone, username=username, password=password, avatar=avatar)
        return redirect(request.args.get("next"))
    except Exception as ex:
        return render_template("register.html", err_msg=str(ex))