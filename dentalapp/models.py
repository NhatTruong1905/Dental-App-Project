from dentalapp import db
from sqlalchemy import Integer, String, DATE, DateTime, Double, Boolean, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
import enum as VAT


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    active = db.Column(Boolean, default=True)

class Person(BaseModel):
    __abstract__ = True

    name = db.Column(String(255), nullable=False)
    birthday = db.Column(DATE, nullable=False)
    phone = db.Column(String(20), nullable=False)
    address = db.column(String(255), nullable=False)

    def __str__(self):
        return self.name

service_paitents = db.Table(
    'service_paitents',
    db.Column('id', Integer, primary_key=True, autoincrement=True),
    db.Column('service_id', Integer, ForeignKey('service.id'), nullable=False),
    db.Column('paitents_id', Integer, ForeignKey('paitents.id'), nullable=False),
)

class Service(BaseModel):
    __tablename__ = "service"
    name = db.Column(String(100), nullable=False)
    price = db.Column(Double, nullable=False)

    def __str__(self):
        return self.name

class Paitents(Person):
    __tablename__ = "paitents"
    services = relationship("Service", secondary="service_paitents", backref="paitents", lazy=True)
    doctor = relationship("Doctor", secondary="appointment_schedule", backref="paitents", lazy=True)

class Doctor(Person):
    __tablename__ = "doctor"


class AppointmentSchedule(BaseModel):
    __tablename__ = "appointment_schedule"
    date_time = db.Column(DateTime, nullable=False)
    id_doctor = db.Column(Integer, ForeignKey('doctor.id'), nullable=False)
    id_paitents = db.Column(Integer, ForeignKey('paitents.id'), nullable=False)
    description = db.Column(String(255), nullable=False)

    __table_args__ = (
        UniqueConstraint('id_doctor', 'date_time')
    )

class Medicine(BaseModel):
    name = db.Column(String(100), nullable=False)
    price = db.Column(Double, nullable=False)
    production_date = db.Column(DATE, nullable=False)
    expiration_date = db.Column(DATE, nullable=False)

    def __str__(self):
        return self.name

class VATEnum(VAT):
    VAT10PER = 10
    VAT2PER = 2

class Bill(BaseModel):
    total_medicine = db.Column(Double, nullable=False)
    total_service = db.Column(Double, nullable=False)
    vat = db.Column(Enum(VATEnum), default=VATEnum.VAT10PER)

class TreatmentCard(BaseModel):
    pass




