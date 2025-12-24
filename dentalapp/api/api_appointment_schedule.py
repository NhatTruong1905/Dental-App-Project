from flask import jsonify, Blueprint, request
from dentalapp.dao import appointment_schedules, appointment_schedule_invoice
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
                    'start_time': str(a.start_time.strftime('%H:%M')),
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


@api_appointment_schedule.route('/api/appointment_schedule/<int:id>/total_services', methods=['GET'])
def calculate_total_services(id):
    total_services = appointment_schedules.culculated_total_service(id)
    services_of_appointment = appointment_schedules.get_services_of_appointment(id)

    try:
        if services_of_appointment:
            result = []
            for s in services_of_appointment:
                result.append(s.service.name)

            return jsonify({
                'service_list': result,
                'total_services': total_services or 0,
            })
        else:
            return jsonify({'ok': True, 'message': "Không khả thi"})
    except Exception as ex:
        return jsonify({'ok': False, 'error': str(ex)})


@api_appointment_schedule.route('/api/appointment_schedule/<int:id>/total_medicines', methods=['GET'])
def culculate_total_medicines(id):
    total_medicines = appointment_schedules.culculated_total_medicine(id)
    medicines_of_appointment = appointment_schedules.get_medicines_of_appointment(id)

    try:
        if medicines_of_appointment:
            result = []
            for m in medicines_of_appointment:
                result.append({
                    'quantity_day': m.quantity_day,
                    'dosage': m.dosage,
                    'medicine_name': m.medicine.name,
                })

            return jsonify({
                'total_medicines': total_medicines or 0,
                'medicine_list': result,
            })
        else:
            return jsonify({'ok': True, 'message': "Không khả thi"})
    except Exception as ex:
        return jsonify({'ok': False, 'error': str(ex)})


@api_appointment_schedule.route('/api/appointment_schedule/invoice', methods=['POST'])
def save_invoice():
    id = int(request.json.get('id'))
    total_service = float(request.json.get('total_service'))
    total_medicine = float(request.json.get('total_medicine'))
    vat = float(request.json.get('vat'))
    total_invoice = float(request.json.get('total_invoice'))

    try:
        appointment_schedule_invoice.saveInvoice(id, total_service, total_medicine, vat, total_invoice)

        return jsonify({'ok': True})
    except Exception as ex:
        return jsonify({'ok': False, 'error': str(ex)})
