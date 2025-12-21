from flask import Blueprint, request
from flask import render_template
from dentalapp.dao import doctors, appointment_schedules

doctors_bp = Blueprint('doctors', __name__)


@doctors_bp.route('/doctors')
def render_doctors():
    data_doctors = doctors.load_doctors()
    return render_template('doctors.html', doctors=data_doctors)


# @doctors_bp.route('/doctors/<int:doctor_id>')
# def render_detail_doctor(doctor_id):
#     doctor = doctors.get_infor_doctor(doctor_id)
#     if not doctor:
#         return "Không tìm thấy bác sĩ", 404
#
#     check_date = request.form.get('check_date')
#     appointment_of_doctor = appointment_schedules.load_appointment_schedules(doctor_id=doctor_id, check_date=check_date)
#
#     if not appointment_of_doctor:
#         return "Không tìm thấy lịch khám"
#
#     return render_template('detail.html', doctor=doctor, appointment_of_doctor=appointment_of_doctor)
