from flask import jsonify, Blueprint, request
from dentalapp.dao import appointment_schedules
from datetime import datetime

api_appointment_schedule = Blueprint('api_appointment_schedule', __name__)


@api_appointment_schedule.route('/api/appointment_schedule', methods=['POST'])
def save_appointment_schedule():
    doctor_id = int(request.json.get('doctor_id'))
    patient_id = int(request.json.get('patient_id'))
    service_id = int(request.json.get('service_id'))
    start_time = datetime.strptime(request.json.get('start_time'), '%Y-%m-%d %H:%M:%S')

    try:
        appointment_schedules.save_appointment_schedule(doctor_id=doctor_id, patient_id=patient_id,
                                                        service_id=service_id, start_time=start_time)
        return jsonify({'ok': True})
    except Exception as ex:
        return jsonify({'ok': False, 'error': str(ex)})


@api_appointment_schedule.route('/api/appointment_schedule/<date>', methods=['GET'])
def get_appointment_schedule(date):
    appointment_successes = appointment_schedules.load_appointment_schedules_success(date)
    try:
        if appointment_successes:
            result = [
                {
                    'id': a.id,
                    'doctor_id': a.doctor_id,
                    'patient_id': a.patient_id,
                    'start_time': str(a.start_time),
                    'end_time': str(a.end_time),
                    'status': a.status.name,
                    'patient_name': a.patient.name,
                    'patient_phone': a.patient.phone,
                }
                for a in appointment_successes
            ]

            return jsonify(result)
        else:
            return jsonify({'ok': False, 'message': "Không có danh sách lịch khám"})
    except Exception as ex:
        return jsonify({'ok': False, 'error': str(ex)})
