from dentalapp import db
from dentalapp.models import AppointmentScheduleMedicine


def save_appointment_schedule_medicine(medicine_id, appointment_schedule_id, price_medicine, dosage, quantity_day):
    appointment_schedule_service = AppointmentScheduleMedicine(medicine_id=medicine_id, appointment_schedule_id=appointment_schedule_id, price_medicine=price_medicine, dosage=dosage, quantity_day=quantity_day)
    db.session.add(appointment_schedule_service)