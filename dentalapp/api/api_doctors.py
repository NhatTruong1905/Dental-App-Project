from flask import Blueprint, request, jsonify
from dentalapp.dao import appointment_schedules, doctors

api_doctors_bp = Blueprint('api_doctors', __name__)


@api_doctors_bp.route('/api/doctors/<int:id>/schedules', methods=['POST'])
def get_appointment_of_doctor(doctor_id):
    check_date = request.form.get('check_date')

    appointment_of_doctor = appointment_schedules.load_appointment_schedules(doctor_id, check_date)
    try:
        if appointment_of_doctor:
            appointments = [{}]
            for a in appointment_of_doctor:
                result = {
                    'doctor_id': a.doctor_id,
                    'patient_id': a.patient_id,
                    'start_time': a.start_time,
                    'end_time': a.end_time,
                    'status': a.status,
                }
                appointments.append(result)

            return jsonify(appointments)
        else:
            return jsonify({"ok": False, "message": "Thất bại"})
    except Exception as e:
        return jsonify({"ok": False, "message": str(e)})


@api_doctors_bp.route('/api/doctors/<int:id>', methods=['GET'])
def get_info_doctor(id):
    infor_doctor = doctors.get_infor_doctor(id)

    try:
        if infor_doctor:
            return jsonify({
                "id": infor_doctor.id,
                "name": infor_doctor.user.name,
                'phone': infor_doctor.user.phone,
                'major': infor_doctor.major,
            })
        else:
            return jsonify({"ok": False, "message": "Thất bại"})
    except Exception as e:
        return jsonify({"ok": False, "message": str(e)})

