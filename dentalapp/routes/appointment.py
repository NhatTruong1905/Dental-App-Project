from flask import render_template, Blueprint
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
