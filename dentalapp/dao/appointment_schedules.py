from datetime import datetime, time, timedelta
from dentalapp import db
from dentalapp.models import AppointmentSchedule, Doctor
from sqlalchemy import and_, func


def count_appointment_schedules(doctor_id, check_date) -> bool:
    return AppointmentSchedule.query.filter(
        and_(
            AppointmentSchedule.doctor_id == doctor_id,
            func.date(AppointmentSchedule.start_time) == check_date
        )
    ).count() < 5


def load_doctors(check_date):
    date = datetime.strptime(check_date, '%Y-%m-%d').date()
    query = db.session.query(AppointmentSchedule.doctor_id).where(
        func.date(AppointmentSchedule.start_time) == date).group_by(AppointmentSchedule.doctor_id).having(
        func.count(AppointmentSchedule.doctor_id) < 5).subquery()

    doctors = db.session.query(Doctor).join(query, query.c.doctor_id == Doctor.id).all()
    # import pdb
    # pdb.set_trace()
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


def add_appointment_schedules(doctor_id, patient_id, check_date, check_time):
    datetime_choice = datetime.combine(check_date, check_time)
    a = AppointmentSchedule(doctor_id=doctor_id, patient_id=patient_id, start_time=time,
                            end_time=datetime_choice + timedelta(minutes=30))

    count = count_appointment_schedules(doctor_id, check_date)
    check = check_duplicate_time(doctor_id, check_date, check_time)
    if count and not check:
        db.session.add(a)
        db.session.commit()
