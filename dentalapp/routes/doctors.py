from flask import Blueprint, request
from flask import render_template
from dentalapp.dao import doctors, appointment_schedules

doctors_bp = Blueprint('doctors', __name__)


@doctors_bp.route('/doctors')
def render_doctors():
    data_doctors = doctors.load_doctors()
    return render_template('doctors.html', doctors=data_doctors)
