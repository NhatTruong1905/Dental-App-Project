from flask import Blueprint, request
from flask import render_template
from dentalapp.dao import doctors

doctors_bp = Blueprint('doctors', __name__)


@doctors_bp.route('/doctors')
def render_doctors():
    data_doctors = [doctor for doctor in doctors.load_doctors(request.args.get('kw'), int(request.args.get("page", 1))) if doctor.active]
    return render_template('doctors.html', doctors=data_doctors, count=doctors.count_doctors())
