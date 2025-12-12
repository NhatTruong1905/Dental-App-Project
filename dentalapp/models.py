from dentalapp import db, app
from sqlalchemy import Column, Integer, String, DATE, DateTime, Double, Boolean, ForeignKey, Enum, UniqueConstraint, Column
from sqlalchemy.orm import relationship
from enum import Enum as VAT


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    active = Column(Boolean, default=True)

class Person(BaseModel):
    __abstract__ = True

    name = Column(String(255), nullable=False)
    birthday = Column(DATE, nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(String(255), nullable=False)

    def __str__(self):
        return self.name

service_paitents = db.Table(
    'service_paitents',
    Column('service_id', Integer, ForeignKey('service.id'), primary_key=True),
    Column('paitents_id', Integer, ForeignKey('paitents.id'), primary_key=True),
)

class Service(BaseModel):
    __tablename__ = "service"
    name = Column(String(100), nullable=False)
    price = Column(Double, nullable=False)

    def __str__(self):
        return self.name

class Paitents(Person):
    __tablename__ = "paitents"
    services = relationship("Service", secondary="service_paitents", backref="paitents", lazy=True)
    medicines = relationship("Medicine", secondary="medicine_paitents", backref="paitents", lazy=True)
    bill = relationship("Bill", backref="paitents", lazy=True)


class Doctor(Person):
    __tablename__ = "doctor"


class AppointmentSchedule(BaseModel):
    __tablename__ = "appointment_schedule"
    date_time = Column(DateTime, nullable=False)
    id_doctor = Column(Integer, ForeignKey('doctor.id'), nullable=False)
    id_paitents = Column(Integer, ForeignKey('paitents.id'), nullable=False)
    description = Column(String(255), nullable=False)

    paitents = relationship("Paitents", backref="apppointment", lazy=True)
    doctor = relationship("Doctor", backref="schedules", lazy=True)

    __table_args__ = (
        UniqueConstraint('id_doctor', 'date_time'),
    )

medicine_paitents = db.Table(
    'medicine_paitents',
    Column('medicine_id', Integer, ForeignKey('medicine.id'), primary_key=True),
    Column('paitents_id', Integer, ForeignKey('paitents.id'), primary_key=True),
)

class Medicine(BaseModel):
    __tablename__ = "medicine"
    name = Column(String(100), nullable=False)
    price = Column(Double, nullable=False)
    production_date = Column(DATE, nullable=False)
    expiration_date = Column(DATE, nullable=False)

    def __str__(self):
        return self.name

class VATEnum(VAT):
    VAT_10_PER = 10
    VAT_2_PER = 2

class Bill(BaseModel):
    total_medicine = Column(Double, nullable=False)
    total_service =  Column(Double, nullable=False)
    total = Column(Double, nullable=False)
    name = Column(String(255), nullable=False)
    vat = Column(Enum(VATEnum), default=VATEnum.VAT_10_PER)
    paitents_id = Column(Integer, ForeignKey('paitents.id'), nullable=False)

class TreatmentCard(BaseModel):
    id_doctor = Column(Integer, ForeignKey('doctor.id'), nullable=False)
    id_paitents = Column(Integer, ForeignKey('paitents.id'), nullable=False)
    description = Column(String(255), nullable=False)

    paitents = relationship("Paitents", backref="treatment", lazy=True)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        db.session.commit()





