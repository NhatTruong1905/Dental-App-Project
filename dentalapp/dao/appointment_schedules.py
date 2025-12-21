from datetime import datetime, time, timedelta
from dentalapp import db
from dentalapp.models import AppointmentSchedule, Doctor
from sqlalchemy import and_, func


def load_doctors(check_date):
    date = datetime.strptime(check_date, '%Y-%m-%d').date()

    query = db.session.query(AppointmentSchedule.doctor_id).where(
        func.date(AppointmentSchedule.start_time) == date).group_by(AppointmentSchedule.doctor_id).having(
        func.count(AppointmentSchedule.doctor_id) >= 5).subquery()

    doctors = db.session.query(Doctor).outerjoin(query, query.c.doctor_id == Doctor.id).where(query.c.doctor_id.is_(None)).all()
    return doctors


def check_duplicate_time(doctor_id, check_date, check_time):
    query = AppointmentSchedule.query.filter(
        and_(
            AppointmentSchedule.doctor_id == doctor_id,
            func.date(AppointmentSchedule.start_time) == check_date,
            func.time(AppointmentSchedule.start_time) == check_time
        )
    ).first()
    if query:
        return False
    return True


def time_of_doctor(doctor_id, check_date):
    check_date = datetime.strptime(check_date, '%Y-%m-%d').date()

    appointments = db.session.query(AppointmentSchedule.start_time).where(
        and_(
            AppointmentSchedule.doctor_id == doctor_id,
            func.date(AppointmentSchedule.start_time) == check_date)).all()

    list_times_of_doctor = []
    for a in appointments:
        list_times_of_doctor.append(a.start_time.strftime('%H:%M')) # 19:00

    return list_times_of_doctor
