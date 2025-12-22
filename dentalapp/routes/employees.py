from flask import Blueprint, render_template
from dentalapp.dao import patients

employees_bp = Blueprint('employees', __name__)


@employees_bp.route('/appointment_employees')
def render_employees():
    return render_template('appointment_employee.html')
