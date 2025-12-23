from flask import Blueprint, render_template, request
from flask_login import current_user

from dentalapp.models import UserRole
from dentalapp.utils import permission
from dentalapp.dao.users import get_current_user
from dentalapp.dao.patients import get_list_patients, create_patient, count_patients

infor_user_bp = Blueprint('infor_user', __name__)

@infor_user_bp.route('/user', methods=['GET'])
@permission()
def render_user():
    user = get_current_user(current_user.id)
    patients = []
    if current_user.user_role in [UserRole.ADMIN, UserRole.STAFF]:
        patients = get_list_patients(full=True, page=int(request.args.get("page", 1)))
    else:
        patients = get_list_patients(full=False)
    return render_template("infor_user.html", user=user, patients=patients, count=count_patients(current_user.user_role in [UserRole.ADMIN, UserRole.STAFF]))

@infor_user_bp.route('/user/infor', methods=['GET'])
@permission()
def render_edit_infor():
    user = get_current_user(current_user.id)
    return render_template("update_infor_user.html", user=user)