from datetime import datetime

from dentalapp import db, app
from sqlalchemy import Column, Integer, String, DATE, DateTime, Double, Boolean, ForeignKey, Enum, UniqueConstraint, Column
from sqlalchemy.orm import relationship
import enum

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    active = Column(Boolean, default=True)

class Person(BaseModel):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    birthday = Column(DATE, nullable=False)
    address = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

class UserRole(enum.Enum):
    ADMIN = 1
    USER = 2
    DOCTOR = 3
    STAFF = 4

class Status(enum.Enum):
    PENDING = 0
    IN_PROGRESS = 1
    COMPLETED = 2

class User(BaseModel):
    __tablename__ = 'user'
    name = Column(String(50), nullable=False)
    avatar = Column(String(100), default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg')
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    user_role = Column(Enum(UserRole), default=UserRole.USER)

class Paitent(Person):
    __tablename__ = 'paitent'


class Doctor(Person):
    __tablename__ = 'doctor'
    major = Column(String(50), nullable=True)

class Service(BaseModel):
    __tablename__ = 'service'
    name = Column(String(100), nullable=False)
    price = Column(Double, nullable=False)

class Medicine(BaseModel):
    __tablename__ = 'medicine'
    name = Column(String(100), nullable=False)
    price = Column(Double, nullable=False)

class AppointmentSchedule(db.Model):
    __tablename__ = 'appointment_schedule'
    id = Column(Integer, primary_key=True, autoincrement=True)
    doctor_id = Column(Integer, ForeignKey("doctor.id"))
    paitent_id = Column(Integer, ForeignKey("paitent.id"))
    datetime = Column(DateTime, nullable=False)
    status = Column(Enum(Status), default=Status.PENDING)

    paitent = relationship("Paitent", backref="appointment_schedule", lazy=True)
    doctor = relationship("Doctor", backref="appointment_schedule", lazy=True)


    __table_args__ = (
        UniqueConstraint('doctor_id', 'datetime'),
    )

class AppointmentScheduleService(db.Model):
    __tablename__ = 'appointment_schedule_service'
    id = Column(Integer, primary_key=True, autoincrement=True)
    appointment_schedule_id = Column(Integer, ForeignKey("appointment_schedule.id"))
    service_id = Column(Integer, ForeignKey("service.id"))
    price_service = Column(Double, nullable=False)

class AppointmentScheduleMedicine(db.Model):
    __tablename__ = 'appointment_schedule_medicine'
    id = Column(Integer, primary_key=True, autoincrement=True)
    appointment_schedule_id = Column(Integer, ForeignKey("appointment_schedule.id"))
    medicine_id = Column(Integer, ForeignKey("medicine.id"))
    price_medicine = Column(Double, nullable=False)
    quantity_day = Column(Integer, nullable=False)
    dosage = Column(Integer, nullable=False)

class TreatmentCard(db.Model):
    __tablename__ = 'treatment_card'
    id = Column(Integer, primary_key=True, autoincrement=True)
    appointment_schedule_id = Column(Integer, ForeignKey("appointment_schedule.id"), unique=True)
    note = Column(String(100), nullable=False)

class Invoice(db.Model):
    __tablename__ = 'invoice'
    id = Column(Integer, primary_key=True, autoincrement=True)
    appointment_schedule_id = Column(Integer, ForeignKey("appointment_schedule.id"), unique=True)
    total_service = Column(Double, nullable=False)
    total_medicine = Column(Double, nullable=False)
    vat = Column(Double, default=10.0)
    total_invoice = Column(Double)

def inser_data():
    # ================== USERS ==================
    admin = User(
        name="Admin",
        username="admin",
        password="123456",
        user_role=UserRole.ADMIN
    )

    doctor_user = User(
        name="Dr John",
        username="doctor1",
        password="123456",
        user_role=UserRole.DOCTOR
    )

    patient_user = User(
        name="Nguyen Van A",
        username="patient1",
        password="123456",
        user_role=UserRole.USER
    )

    db.session.add_all([admin, doctor_user, patient_user])
    db.session.commit()

    # ================== DOCTOR ==================
    doctor = Doctor(
        first_name="John",
        last_name="Doe",
        birthday="1985-03-20",
        address="HCM City",
        phone="0909555666",
        major="Orthodontics",
        user_id=doctor_user.id
    )

    # ================== PATIENT ==================
    paitent = Paitent(
        first_name="Van",
        last_name="Nguyen",
        birthday="2000-05-10",
        address="HCM City",
        phone="0909123456",
        user_id=patient_user.id
    )

    db.session.add_all([doctor, paitent])
    db.session.commit()

    # ================== SERVICES ==================
    service1 = Service(name="Tooth Cleaning", price=200000)
    service2 = Service(name="Tooth Filling", price=500000)

    db.session.add_all([service1, service2])
    db.session.commit()

    # ================== MEDICINES ==================
    medicine1 = Medicine(name="Painkiller", price=50000)
    medicine2 = Medicine(name="Antibiotic", price=100000)

    db.session.add_all([medicine1, medicine2])
    db.session.commit()

    # ================== APPOINTMENT ==================
    appointment = AppointmentSchedule(
        doctor_id=doctor.id,
        paitent_id=paitent.id,
        datetime=datetime(2025, 1, 15, 9, 0),
        status=Status.PENDING
    )

    db.session.add(appointment)
    db.session.commit()

    # ================== APPOINTMENT - SERVICES ==================
    aps = AppointmentScheduleService(
        appointment_schedule_id=appointment.id,
        service_id=service1.id,
        price_service=service1.price
    )

    # ================== APPOINTMENT - MEDICINES ==================
    apm = AppointmentScheduleMedicine(
        appointment_schedule_id=appointment.id,
        medicine_id=medicine2.id,
        price_medicine=medicine2.price,
        quantity_day=5,
        dosage=2
    )

    db.session.add_all([aps, apm])
    db.session.commit()

    # ================== TREATMENT CARD ==================
    treatment_card = TreatmentCard(
        appointment_schedule_id=appointment.id,
        note="Patient has mild tooth decay"
    )

    db.session.add(treatment_card)
    db.session.commit()

    # ================== INVOICE ==================
    total_service = service1.price
    total_medicine = medicine2.price * 5
    vat = 0.1
    total_invoice = (total_service + total_medicine) * (1 + vat)

    invoice = Invoice(
        appointment_schedule_id=appointment.id,
        total_service=total_service,
        total_medicine=total_medicine,
        vat=10,
        total_invoice=total_invoice
    )

    db.session.add(invoice)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        p = Paitent.query.get(1)
        print(p.appointment_schedule[0].__dict__)





