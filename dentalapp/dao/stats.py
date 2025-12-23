from dentalapp.models import AppointmentSchedule, Invoice, Doctor, User
from dentalapp import db, app
from sqlalchemy import func


# def revenue_by_doctor1(kw=None):
#     return (db.session.query(AppointmentSchedule.doctor_id, func.sum(Invoice.total_invoice).label("invoice_amount"))
#             .join(AppointmentSchedule, Invoice.appointment_schedule_id == AppointmentSchedule.id )
#             .group_by(AppointmentSchedule.doctor_id))
# def revenue_by_doctor2(doctor_id, check_date):
#     return (db.session.query(func.extract("day", AppointmentSchedule.start_time), func.sum(Invoice.total_invoice).label("invoice_amount")).
#             join(AppointmentSchedule, Invoice.appointment_schedule_id == AppointmentSchedule.id )
#             .filter(AppointmentSchedule.doctor_id == doctor_id).group_by(func.extract("day", AppointmentSchedule.start_time)).all())

def revenue_by_doctor_month():
    return (
        db.session.query(
            func.extract("month", AppointmentSchedule.start_time).label("month"),
            func.sum(Invoice.total_invoice).label("total_revenue")
        )
        .join(AppointmentSchedule, Invoice.appointment_schedule_id == AppointmentSchedule.id)
        # .filter(
        #     func.extract("month",AppointmentSchedule.start_time) == check_date
        # )
        .group_by(
            func.extract("month", AppointmentSchedule.start_time)
        )
        .all()
    )

def revenue_by_doctor_day():
    return (
        db.session.query(
            func.extract("day", AppointmentSchedule.start_time).label("day"),
            func.sum(Invoice.total_invoice).label("total_revenue")
        )
        .join(AppointmentSchedule, Invoice.appointment_schedule_id == AppointmentSchedule.id)
        # .filter(
        #     func.extract("day",AppointmentSchedule.start_time) == check_date
        # )
        .group_by(
            func.extract("day", AppointmentSchedule.start_time)
        )
        .all()
    )

def revenue_by_doctor():
    return (
        db.session.query(
            Doctor.id.label("doctor_id"),
            User.name.label("doctor_name"),
            func.sum(Invoice.total_invoice).label("total_revenue")
        )
        .join(AppointmentSchedule, AppointmentSchedule.doctor_id == Doctor.id)
        .join(Invoice, Invoice.appointment_schedule_id == AppointmentSchedule.id)
        .join(User, User.id == Doctor.id)
        # .filter(
        #     Doctor.id == doctor_id
        # )
        .group_by(
            Doctor.id,
            User.name,
        )
        .all()
    )



# if __name__ == '__main__':
#     with app.app_context():
#          print(revenue_by_doctor2(5,'2025-01-01'))
