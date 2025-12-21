from flask import render_template, Blueprint
from flask_login import current_user
from dentalapp.dao.services import load_services

appointment_bp = Blueprint('appointment', __name__)


@appointment_bp.route('/appointment')
def render_appointment():
    services = load_services()
    return render_template('appointment.html', services=services, user_id=current_user.id)