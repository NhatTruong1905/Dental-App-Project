from dentalapp import db
import sqlalchemy as sql
import enum as VAT


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(sql.Integer, primary_key=True, autoincrement=True)
    active = db.Column(sql.Boolean, default=True)

class Person(BaseModel):
    __abstract__ = True

    name = db.Column(sql.String(255), nullable=False)
    birthday = db.Column(sql.DATE, nullable=False)
    phone = db.Column(sql.String(20), nullable=False)
    address = db.column(sql.String(255), nullable=False)

class Service(BaseModel):
    name = db.Column(sql.String(100), nullable=False)
    price = db.Column(sql.Double, nullable=False)

class Paitents(Person):
    pass

class Doctor(Person):
    pass

class Medicine(BaseModel):
    name = db.Column(sql.String(100), nullable=False)
    price = db.Column(sql.Double, nullable=False)
    production_date = db.Column(sql.DATE, nullable=False)
    expiration_date = db.Column(sql.DATE, nullable=False)

class VATEnum(VAT):
    VAT10PER = 10
    VAT2PER = 2

class Bill(BaseModel):
    total_medicine = db.Column(sql.Double, nullable=False)
    total_service = db.Column(sql.Double, nullable=False)
    vat = db.Column(sql.Enum(VATEnum), default=VATEnum.VAT10PER)

class TreatmentCard(BaseModel):
    pass




