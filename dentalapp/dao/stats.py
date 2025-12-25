from dentalapp.models import AppointmentSchedule, Invoice, Doctor, User
from dentalapp import db, app
from sqlalchemy import func, null
from datetime import datetime


def revenue_by_doctor_month(time,year):
    query = (
        db.session.query(
            func.extract("month", AppointmentSchedule.start_time).label("month"),
            func.sum(Invoice.total_invoice).label("total_revenue")
        )
        .join(AppointmentSchedule, Invoice.appointment_schedule_id == AppointmentSchedule.id)
        .filter(
            func.extract("year",AppointmentSchedule.start_time) == year,
        )
        .group_by(
            func.extract("month", AppointmentSchedule.start_time)
        )
    )

    if time:
        query = query.filter(
            func.extract("month", AppointmentSchedule.start_time) == time
        )
    return query.all()

def revenue_by_doctor_day(time, year):
    query = (
        db.session.query(
            func.extract("day", AppointmentSchedule.start_time).label("day"),
            func.sum(Invoice.total_invoice).label("total_revenue")
        )
        .join(AppointmentSchedule, Invoice.appointment_schedule_id == AppointmentSchedule.id)
        .filter(
            func.extract("year",AppointmentSchedule.start_time) == year,
        )
        .group_by(
            func.extract("day", AppointmentSchedule.start_time)
        )
    )

    if time:
        query = query.filter(
            func.extract("month", AppointmentSchedule.start_time) == time
        )
    return query.all()

def revenue_by_doctor(time, year):
    query = (
        db.session.query(
            Doctor.id.label("doctor_id"),
            User.name.label("doctor_name"),
            func.sum(Invoice.total_invoice).label("total_revenue")
        )
        .join(AppointmentSchedule, AppointmentSchedule.doctor_id == Doctor.id)
        .join(Invoice, Invoice.appointment_schedule_id == AppointmentSchedule.id)
        .join(User, User.id == Doctor.id)
        .filter(
            func.extract("year", AppointmentSchedule.start_time) == year
        )
        .group_by(
            Doctor.id,
            User.name,
        )
    )
    if time:
        query = query.filter(
            func.extract("month", AppointmentSchedule.start_time) == time
        )
    return query.all()



# if __name__ == '__main__':
#     with app.app_context():
#          print(revenue_by_doctor2(5,'2025-01-01'))
