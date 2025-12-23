from dentalapp import db
from dentalapp.models import AppointmentScheduleService


def save_appointment_schedule_service(service_id, appointment_schedule_id, price_service, is_commit=False):
    appointment_schedule_service = AppointmentScheduleService(service_id=service_id, appointment_schedule_id=appointment_schedule_id, price_service=price_service)
    db.session.add(appointment_schedule_service)
    if is_commit:
        db.session.commit()