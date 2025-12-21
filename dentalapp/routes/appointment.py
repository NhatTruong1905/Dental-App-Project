from flask import render_template, Blueprint


appointment_bp = Blueprint('appointment', __name__)


@appointment_bp.route('/appointment')
def render_appointment():
    return render_template('appointment.html')
