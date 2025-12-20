from flask import Blueprint, render_template
from flask_login import current_user
from dentalapp.utils import permission
from dentalapp.dao.users import get_current_user
from dentalapp.dao.patients import get_list_patients

infor_user_bp = Blueprint('infor_user', __name__)

@infor_user_bp.route('/user', methods=['GET'])
@permission()
def render_user():
    user = get_current_user(current_user.id)
    patients = get_list_patients()
    return render_template("infor_user.html", user=user, patients=patients)

@infor_user_bp.route('/user/infor', methods=['GET'])
@permission()
def render_edit_infor():
    user = get_current_user(current_user.id)
    return render_template("update_infor_user.html", user=user)