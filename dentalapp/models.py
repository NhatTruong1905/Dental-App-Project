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
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    birthday = Column(DATE, nullable=False)
    address = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=False)

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

class Paitents(BaseModel):
    __tablename__ = 'paitents'
    id = Column(Integer, ForeignKey("user.id"), primary_key=True, autoincrement=True)


class Doctor(BaseModel):
    __tablename__ = 'doctor'
    id = Column(Integer, ForeignKey("user.id"), primary_key=True, autoincrement=True)
    major = Column(String(50), nullable=True)

class Service(BaseModel):
    __tablename__ = 'service'
    name = Column(String(100), nullable=False)
    price = Column(Double, nullable=False)

class Medicine(BaseModel):
    __tablename__ = 'medicine'
    name = Column(String(100), nullable=False)
    price = Column(Double, nullable=False)

class AppointmentSchedule(BaseModel):
    __tablename__ = 'appointment_schedule'
    doctor_id = Column(Integer, ForeignKey("doctor.id"))
    paitents_id = Column(Integer, ForeignKey("paitents.id"))
    datetime = Column(DateTime, nullable=False)
    status = Column(Enum(Status), default=Status.PENDING)

    __table_args__ = (
        UniqueConstraint('doctor_id', 'datetime'),
    )

class AppointmentScheduleService(BaseModel):
    __tablename__ = 'appointment_schedule_service'
    appointment_schedule_id = Column(Integer, ForeignKey("appointment_schedule.id"))
    service_id = Column(Integer, ForeignKey("service.id"))
    price_service = Column(Double, nullable=False)

class AppointmentScheduleMedicine(BaseModel):
    __tablename__ = 'appointment_schedule_medicine'
    appointment_schedule_id = Column(Integer, ForeignKey("appointment_schedule.id"))
    medicine_id = Column(Integer, ForeignKey("medicine.id"))
    price_medicine = Column(Double, nullable=False)
    quantity_day = Column(Integer, nullable=False)
    dosage = Column(Integer, nullable=False)

class TreatmentCard(BaseModel):
    __tablename__ = 'treatment_card'
    appointment_schedule_id = Column(Integer, ForeignKey("appointment_schedule.id"))
    note = Column(String(100), nullable=False)

class Invoice(BaseModel):
    __tablename__ = 'invoice'
    appointment_schedule_id = Column(Integer, ForeignKey("appointment_schedule.id"))

    total_service = Column(Double, nullable=False)
    total_medicine = Column(Double, nullable=False)
    vat = Column(Double, default=10.0)
    total_invoice = Column(Double)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        db.session.commit()





