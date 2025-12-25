from dentalapp.models import Patient
from flask_login import current_user
from dentalapp import db, app
from sqlalchemy import and_


def create_patient(name, phone, birthday, address, medical_history):
    patient = Patient(name=name, phone=phone, birthday=birthday, address=address, medical_history=medical_history,
                      user_id=current_user.id)
    db.session.add(patient)
    db.session.commit()


def get_patient(id):
    patient = Patient.query.get(id)
    return patient


def get_list_patients(full=False, page=1):
    query = Patient.query

    if not full:
        query = query.filter(Patient.user_id == current_user.id, Patient.active.is_(True))
    else:
        query = query.filter(Patient.active.is_(True))

    if page:
        page_size = app.config['PAGE_SIZE']
        start = (page - 1) * page_size
        query = query.slice(start, start + page_size)

    return query.all()


def count_patients(full=False):
    return Patient.query.filter(Patient.active.is_(True)).count() if full \
        else Patient.query.filter(and_(Patient.active.is_(True), Patient.user_id == current_user.id)).count()


def delete_soft_patient(id):
    patient = Patient.query.get(id)
    patient.active = False
    db.session.commit()
