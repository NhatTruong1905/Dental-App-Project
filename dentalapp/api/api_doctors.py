from flask import Blueprint, request, jsonify
from dentalapp.dao import appointment_schedules, doctors

api_doctors_bp = Blueprint('api_doctors', __name__)


@api_doctors_bp.route('/api/doctors/check-date', methods=['GET'])
def get_doctor_of_date():
    check_date = request.args.get('date')
    if not check_date:
        return jsonify([{}])

    doctors = appointment_schedules.load_doctors(check_date)
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
