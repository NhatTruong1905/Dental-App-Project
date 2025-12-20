from flask import Blueprint
from flask import render_template
from dentalapp.dao import doctors, appointment_schedules

doctors_bp = Blueprint('doctors', __name__)


@doctors_bp.route('/doctors')
def render_doctors():
    data_doctors = doctors.load_doctors()
    return render_template('doctors.html', doctors=data_doctors)


@doctors_bp.route('/doctors/<int:doctor_id>')
def render_detail_doctor(doctor_id):
    doctor = doctors.get_infor_doctor(doctor_id)

    if not doctor:
        return "Không tìm thấy bác sĩ", 404

    return render_template('detail.html', doctor=doctor)
