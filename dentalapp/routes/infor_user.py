from flask import Blueprint, render_template, request
from flask_login import current_user

from dentalapp import app
from dentalapp.models import UserRole
from dentalapp.utils import permission
from dentalapp.dao.users import get_current_user
from dentalapp.dao.patients import get_list_patients, create_patient, count_patients
import math

infor_user_bp = Blueprint('infor_user', __name__)

@infor_user_bp.route('/user', methods=['GET'])
@permission()
def render_user():
    user = get_current_user(current_user.id)
    if current_user.user_role in [UserRole.ADMIN, UserRole.STAFF]:
        patients = get_list_patients(full=True, page=int(request.args.get("page", 1)))
    else:
        patients = get_list_patients(full=False)
    pages = math.ceil(count_patients(current_user.user_role in [UserRole.ADMIN, UserRole.STAFF]) / app.config['PAGE_SIZE'])
    return render_template("infor_user.html", user=user, patients=patients, pages=pages)

@infor_user_bp.route('/user/infor', methods=['GET'])
@permission()
def render_edit_infor():
    user = get_current_user(current_user.id)
    return render_template("update_infor_user.html", user=user)