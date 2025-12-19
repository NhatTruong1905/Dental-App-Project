from datetime import datetime, time, timedelta
from dentalapp import db
from dentalapp.models import AppointmentSchedule
from sqlalchemy import func, and_


def count_appointment_schedules(doctor_id, check_datetime):
    return AppointmentSchedule.query.filter(
        and_(
            AppointmentSchedule.doctor_id == doctor_id,
            func.date(AppointmentSchedule.start_time) == check_datetime
        )
    ).count() <= 5


def load_appointment_schedules(doctor_id, check_date):
    appointment_of_doctors = count_appointment_schedules(doctor_id=doctor_id, check_datetime=check_date)
    query = AppointmentSchedule.query

    if appointment_of_doctors:
        query = query.filter(AppointmentSchedule.doctor_id == doctor_id)

    return query.all()


def check_duplicate_appointment(doctor_id, check_datetime):
    query = AppointmentSchedule.query.filter(
        and_(
            AppointmentSchedule.doctor_id == doctor_id,
            func.date(AppointmentSchedule.start_time) == check_datetime
        )
    )
    if query:
        return False
    return True


def add_appointment_schedules(doctor_id, check_date):
    date_choice = datetime.combine(check_date, datetime.now().time())
    a = AppointmentSchedule(doctor_id=doctor_id, start_time=time, end_time=date_choice + timedelta(minutes=30))

    count = count_appointment_schedules(doctor_id, check_date)
    if count:
        db.session.add(a)
        db.session.commit()
