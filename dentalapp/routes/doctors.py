from flask import Blueprint, request
from flask import render_template

from dentalapp import app
from dentalapp.dao import doctors
import math

doctors_bp = Blueprint('doctors', __name__)


@doctors_bp.route('/doctors')
def render_doctors():
    data_doctors = [doctor for doctor in doctors.load_doctors(request.args.get('kw'), int(request.args.get("page", 1))) if doctor.active]
    pages = math.ceil(doctors.count_doctors() / app.config['PAGE_SIZE'])
    return render_template('doctors.html', doctors=data_doctors, pages=pages)
