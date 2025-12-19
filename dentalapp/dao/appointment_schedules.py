from dentalapp.models import AppointmentSchedule
from sqlalchemy import func, and_


def count_appointment_schedules(doctor_id, check_date):
    return AppointmentSchedule.query.filter(
        and_(
            AppointmentSchedule.doctor_id == doctor_id,
            func.date(AppointmentSchedule.start_time) == check_date
        )
    ).count() <= 5


def load_appointment_schedules(doctor_id, check_date):
    appointment_of_doctors = count_appointment_schedules(doctor_id=doctor_id, check_date=check_date)
    query = AppointmentSchedule.query

    if appointment_of_doctors:
        query = query.filter(AppointmentSchedule.doctor_id == doctor_id)

    return query.all()

# def book_appointment_schedule(doctor_id=None, date_choice=None):
#     query = AppointmentSchedule.query
#
#     return query.all()
