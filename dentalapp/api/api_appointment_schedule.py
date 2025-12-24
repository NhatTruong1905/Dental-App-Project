from flask import jsonify, Blueprint, request
from flask_login import current_user

from dentalapp import db
from dentalapp.dao import appointment_schedules, appointment_schedule_service, appointment_schedule_medicine, treatment_card
from datetime import datetime

from dentalapp.models import UserRole, Status
from dentalapp.utils import permission

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


@api_appointment_schedule.route("/api/appointment_schedule/<int:id>", methods=["DELETE"])
@permission({
    'roles': [UserRole.DOCTOR],
    'access': False
})
def delete_appointment_schedule(id):
    try:
        appointment = appointment_schedules.get_appointment_schedule(id)
        if not appointment:
            return jsonify({'ok': False, 'error': 'appointment not found'})

        can_delete = False
        if current_user.user_role in [UserRole.ADMIN, UserRole.STAFF]:
            can_delete = True
        elif current_user.user_role == UserRole.USER and current_user.id == appointment.patient.user_id:
            can_delete = True

        if not can_delete:
            return jsonify({"ok": False, "error": "You can't delete this appointment"})

        res = appointment_schedules.delete_appointment_schedules(id)
        return jsonify({
            'ok': True,
            'data': {
                'id': res.id,
                'start_time': res.start_time.strftime('%Y-%m-%d %H:%M:%S')
            },
            'message': 'Delete success'
        })
    except Exception as ex:
        return jsonify({"ok": False, "error": str(ex)})

@api_appointment_schedule.route("/api/appointment_doctor/<int:id>", methods=["POST"])
@permission({
    'roles': [UserRole.DOCTOR],
    'access': True
})
def confirm_appointment_doctor(id):
    services = request.json.get('services')
    medicines = request.json.get('medicines')
    note = request.json.get('note')

    try:
        for service in services:
             appointment_schedule_service.save_appointment_schedule_service(**service)
        for medicine in medicines:
            appointment_schedule_medicine.save_appointment_schedule_medicine(**medicine)
        treatment_card.save_treatment_card(**note)

        appointment = appointment_schedules.get_appointment_schedule(id)
        appointment.status = Status.COMPLETED

        db.session.commit()

        return jsonify({'ok': True, "message": "Save success"})

    except Exception as ex:
        return jsonify({'ok': False, 'error': str(ex)})
