from dentalapp.models import Patient
from flask_login import current_user
from dentalapp import db


def create_patient(name, phone, birthday, address, medical_history):
    patient = Patient(name=name, phone=phone, birthday=birthday, address=address, medical_history=medical_history, user_id=current_user.id)
    db.session.add(patient)
    db.session.commit()

def get_patient(id):
    patient = Patient.query.get(id)
    return patient

def get_list_patients():
    return [patient for patient in current_user.patients if patient.active]

def delete_soft_patient(id):
    patient = Patient.query.get(id)
    patient.active = False
    db.session.commit()