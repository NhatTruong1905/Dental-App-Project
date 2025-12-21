from flask import Blueprint, request, jsonify
from dentalapp.dao import appointment_schedules, doctors

api_doctors_bp = Blueprint('api_doctors', __name__)


@api_doctors_bp.route('/api/doctors/<date>', methods=['GET'])
def get_doctor_of_date(date):
    doctors = appointment_schedules.load_doctors(date)
    try:
        if doctors:
            result = [
                {
                    "id": doctor.id,
                    "name": doctor.user.name,
                    'phone': doctor.user.phone,
                    'major': doctor.major,
                }
                for doctor in doctors
            ]

            return jsonify(result)
        else:
            return jsonify({"ok": False, "message": "Thất bại"})
    except Exception as e:
        return jsonify({"ok": False, "message": str(e)})


@api_doctors_bp.route('/api/doctors/<int:id>/<date>/times', methods=['GET'])
def get_times_of_doctor(id, date):
    list_times_of_doctor = appointment_schedules.time_of_doctor(id, date)
    try:
        if list_times_of_doctor:
            result = {
                "time": [time for time in list_times_of_doctor]
            }

            return jsonify(result)
        else:
            return jsonify({"ok": False, "message": "Thất bại"})
    except Exception as e:
        return jsonify({"ok": False, "message": str(e)})
