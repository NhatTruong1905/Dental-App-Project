from datetime import datetime

from flask import Blueprint, request
from dentalapp.dao import appointment_schedules

api_doctors_bp = Blueprint('api_doctors', __name__)


@api_doctors_bp.route('/api/appointment_schedules', methods=['POST'])
def add_appointment_of_doctor():
    doctor_id = request.args.get('doctor_id')
    check_date = request.form.get('check_date')

    if not check_date:
        check_date = datetime.now().date()

    appointment_of_doctor = appointment_schedules.count_appointment_schedules(doctor_id, check_date)

    if appointment_of_doctor:
        pass
