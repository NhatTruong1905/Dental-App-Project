from dentalapp import db, app
from sqlalchemy import Column, Integer, String, DATE, DateTime, Double, Boolean, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
import enum
import os
import json


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    active = Column(Boolean, default=True)


class Person(BaseModel):
    __abstract__ = True
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    birthday = Column(DATE, nullable=False)
    address = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    def __str__(self):
        return self.first_name + " " + self.last_name


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
    phone = Column(String(50), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg')
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    user_role = Column(Enum(UserRole), default=UserRole.USER)


class Patients(Person):
    __tablename__ = 'patients'
    appointment_schedules = relationship("AppointmentSchedule", backref="patients", lazy=True)


class Doctor(Person):
    __tablename__ = 'doctor'
    major = Column(String(50), nullable=True)
    appointment_schedules = relationship("AppointmentSchedule", backref="doctor", lazy=True)


class Service(BaseModel):
    __tablename__ = 'service'
    name = Column(String(100), nullable=False)
    price = Column(Double, nullable=False)
    appointment_schedule_services = relationship("AppointmentScheduleService", backref="service", lazy=True)


class Medicine(BaseModel):
    __tablename__ = 'medicine'
    name = Column(String(100), nullable=False)
    price = Column(Double, nullable=False)
    production_date = Column(DATE, nullable=False)
    expiration_date = Column(DATE, nullable=False)
    appointment_schedule_medicines = relationship("AppointmentScheduleMedicine", backref="medicine", lazy=True)


class AppointmentSchedule(db.Model):
    __tablename__ = 'appointment_schedule'
    id = Column(Integer, primary_key=True, autoincrement=True)
    doctor_id = Column(Integer, ForeignKey("doctor.id"))
    paitent_id = Column(Integer, ForeignKey("patients.id"))
    datetime = Column(DateTime, nullable=False)
    status = Column(Enum(Status), default=Status.PENDING)

    invoice = relationship("Invoice", backref="appointment_schedule", lazy=True, uselist=False)
    treatment_card = relationship("TreatmentCard", backref="appointment_schedule", lazy=True, uselist=False)

    appointment_schedule_services = relationship("AppointmentScheduleService", backref="appointment_schedule",
                                                 lazy=True)
    appointment_schedule_medicines = relationship("AppointmentScheduleMedicine", backref="appointment_schedule",
                                                  lazy=True)

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

def create_db():
    with app.app_context():
        db.create_all()
        db.session.commit()

def insert_service(services):
    with open(os.path.join(app.root_path, 'data/services.json'), encoding="utf-8") as f:
        data = json.load(f)
    services = []
    for s in data:
        services.append(Service(**s))
    with app.app_context():
        db.session.add_all(services)
        db.session.commit()

def insert_medicine(medicines):
    with open(os.path.join(app.root_path, 'data/medicines.json'), encoding="utf-8") as f:
        data = json.load(f)
    medicines = []
    for m in data:
        medicines.append(Medicine(**m))
    with app.app_context():
        db.session.add_all(medicines)
        db.session.commit()


if __name__ == '__main__':
    create_db()
    insert_service("services.json")
    insert_medicine("medicines.json")
