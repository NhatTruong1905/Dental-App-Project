from flask import Blueprint, render_template, request, redirect, jsonify
from dentalapp.dao.users import validate_phone
from flask_login import current_user
from dentalapp.dao import patients
from dentalapp.models import UserRole
from dentalapp.utils import permission

patient_bp = Blueprint('patient', __name__)


@patient_bp.route('/patients/new', methods=["GET"])
@permission()
def render_create_patient():
    return render_template("register_patient.html")

@patient_bp.route('/patients', methods=['POST'])
@permission()
def create_patient():
    name = request.form.get("name")
    phone = request.form.get("phone")
    if not validate_phone(phone):
        return render_template("register_patient.html", err_msg="Số điện thoại không hơp lệ!")
    birthday = request.form.get("birthday")
    address = request.form.get("address")
    medical_history = request.form.get("medical_history")
    try:
        patients.create_patient(name=name, phone=phone, birthday=birthday, address=address, medical_history=medical_history)
        return redirect(request.args.get("next"))
    except Exception as ex:
        return render_template("register_patient.html", err_msg="Lỗi hệ thống vui lòng thử lại sau!")


@patient_bp.route("/patients/<int:id>", methods=["GET"])
@permission()
def patients_profile(id):
    patient = patients.get_patient(id)
    if patient.user.id != current_user.id and current_user.user_role not in [UserRole.ADMIN, UserRole.STAFF] or not patient.active:
        patient = None
    return render_template("patient_profile.html", patient=patient)
