from datetime import datetime, time, timedelta
from dentalapp import db, app
from dentalapp.models import AppointmentSchedule, Doctor, Service, Patient, UserRole, Status, User
from sqlalchemy import and_, func, or_
from dentalapp.dao import appointment_schedule_service
from flask_login import current_user


def load_doctors(check_date):
    date = datetime.strptime(check_date, '%Y-%m-%d').date()

    query = db.session.query(AppointmentSchedule.doctor_id).where(
        func.date(AppointmentSchedule.start_time) == date).group_by(AppointmentSchedule.doctor_id).having(
        func.count(AppointmentSchedule.doctor_id) >= 5).subquery()

    doctors = db.session.query(Doctor).outerjoin(query, query.c.doctor_id == Doctor.id).where(
        query.c.doctor_id.is_(None)).all()
    return doctors


def time_of_doctor(doctor_id, check_date):
    check_date = datetime.strptime(check_date, '%Y-%m-%d').date()

    appointments = db.session.query(AppointmentSchedule.start_time).where(
        and_(
            AppointmentSchedule.doctor_id == doctor_id,
            func.date(AppointmentSchedule.start_time) == check_date)).all()

    list_times_of_doctor = []
    for a in appointments:
        list_times_of_doctor.append(a.start_time.strftime('%H:%M'))

    if check_date == datetime.today().date():
        now = datetime.now()

        time_start_morning = datetime.combine(check_date, time(7, 0))
        while time_start_morning < min(now - timedelta(minutes=10), datetime.combine(check_date, time(11, 31))):
            list_times_of_doctor.append(time_start_morning.strftime('%H:%M'))
            time_start_morning += timedelta(minutes=30)

        time_start_afternoon = datetime.combine(check_date, time(13, 0))
        while time_start_afternoon < min(now - timedelta(minutes=10), datetime.combine(check_date, time(17, 31))):
            list_times_of_doctor.append(time_start_afternoon.strftime('%H:%M'))
            time_start_afternoon += timedelta(minutes=30)

    return list_times_of_doctor


def save_appointment_schedule(doctor_id, patient_id, start_time, service_id):
    appointment_schedule = AppointmentSchedule(doctor_id=doctor_id, patient_id=patient_id, start_time=start_time,
                                               end_time=start_time + timedelta(minutes=30))
    db.session.add(appointment_schedule)
    db.session.flush()
    price_service = Service.query.get(service_id).price
    appointment_schedule_service.save_appointment_schedule_service(appointment_schedule_id=appointment_schedule.id,
                                                                   service_id=service_id, price_service=price_service)
    db.session.commit()


def find_patient(date_success, phone=None):
    date_success = datetime.strptime(date_success, '%Y-%m-%d').date()

    query = db.session.query(AppointmentSchedule.patient_id).where(
        and_(
            AppointmentSchedule.status == "SUCCESS",
            func.date(AppointmentSchedule.start_time) == date_success)).subquery()

    patients = db.session.query(Patient).join(query, query.c.patient_id == Patient.id).where(
        Patient.phone == phone).all()

    return patients


def load_appointment_schedules_success(check_date):
    check_date = datetime.strptime(check_date, '%Y-%m-%d').date()
    query = db.session.query(AppointmentSchedule).filter(
        and_(
            AppointmentSchedule.status == "SUCCESS",
            func.date(AppointmentSchedule.start_time) == check_date)).all()

    return query

def load_appointment_schedules(date=None, page=1):
    query = AppointmentSchedule.query
    if date:
        query = query.filter(func.date(AppointmentSchedule.start_time) == date)

    if current_user.user_role in [UserRole.ADMIN, UserRole.STAFF]:
        pass
    elif current_user.user_role == UserRole.DOCTOR:
        query = query.filter(and_(AppointmentSchedule.doctor_id == current_user.id, AppointmentSchedule.status.in_([Status.PENDING, Status.IN_PROGRESS])))
    else:
        query = query.join(Patient, AppointmentSchedule.patient_id == Patient.id).filter(Patient.user_id == current_user.id)
    count = query.count()
    query = query.order_by(AppointmentSchedule.start_time)
    start = (page - 1) * app.config['PAGE_SIZE']
    query = query.slice(start, start + app.config['PAGE_SIZE'])
    return query.all(), count

def delete_appointment_schedules(id):
    appointment_schedule = AppointmentSchedule.query.get(id)
    db.session.delete(appointment_schedule)
    db.session.commit()
    return appointment_schedule


def get_appointment_schedule(id):
    appointment = AppointmentSchedule.query.get(id)

    if not appointment:
        return None
    if current_user.user_role in [UserRole.ADMIN, UserRole.STAFF]:
        return appointment
    if current_user.user_role == UserRole.DOCTOR and appointment.doctor_id == current_user.id:
        return appointment
    if current_user.user_role == UserRole.USER and appointment.patient.user_id == current_user.id:
        return appointment

    return None

