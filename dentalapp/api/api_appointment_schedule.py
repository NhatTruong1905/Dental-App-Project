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
        appointment_schedules.save_appointment_schedule(doctor_id=doctor_id, patient_id=patient_id, service_id=service_id, start_time=start_time)
        return jsonify({'ok': True})
    except Exception as ex:
        return jsonify({'ok': False, 'error': str(ex)})

