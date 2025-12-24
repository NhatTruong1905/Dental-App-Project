import math

from flask import render_template, Blueprint, request, session

from dentalapp import app
from dentalapp.dao.appointment_schedules import load_appointment_schedules, get_appointment_schedule
from dentalapp.dao.services import load_services
from dentalapp.dao.medicines import load_medicines
from dentalapp.utils import permission
from dentalapp.models import UserRole


appointment_bp = Blueprint('appointment', __name__)


@appointment_bp.route('/appointment')
@permission({
    "roles": [UserRole.DOCTOR],
    "access": False
})
def render_appointment():
    return render_template('appointment.html')

@appointment_bp.route('/appointments', methods=['GET'])
@permission()
def render_list_appointment():
    appointments, count = load_appointment_schedules(request.args.get("date"), int(request.args.get("page", 1)))
    pages = math.ceil(count / app.config['PAGE_SIZE'])
    return render_template('list_appointments.html', appointments=appointments, pages=pages)


@appointment_bp.route('/appointments/<int:id>', methods=['GET'])
@permission()
def get_appointment(id):
    appointment = get_appointment_schedule(id)
    return render_template("detail_appointments.html", appointment=appointment)

@appointment_bp.route('/appointments_doctor/<int:id>', methods=['GET'])
@permission({
    "roles": [UserRole.DOCTOR],
    "access": True
})
def render_appointment_doctor(id):
    appointment = get_appointment_schedule(id)
    service = appointment.appointment_schedule_services[0].service
    services = load_services(page=None)
    medicines = load_medicines()
    return render_template('appointments_doctor.html', appointment=appointment, service=service, services=services, medicines=medicines)
