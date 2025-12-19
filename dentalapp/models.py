from dentalapp import db, app
from sqlalchemy import Column, Integer, String, DATE, DateTime, Double, Boolean, ForeignKey, Enum, UniqueConstraint, Text
from sqlalchemy.orm import relationship
import enum
from flask_login import UserMixin
from datetime import datetime, date, timedelta, time
import random
from dentalapp.utils import hash_password


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    active = Column(Boolean, default=True)


class UserRole(enum.Enum):
    ADMIN = 1
    USER = 2
    DOCTOR = 3
    STAFF = 4


class Status(enum.Enum):
    PENDING = 0
    IN_PROGRESS = 1
    COMPLETED = 2


class User(BaseModel, UserMixin):
    __tablename__ = 'user'
    name = Column(String(50), nullable=False)
    phone = Column(String(10), nullable=False)
    avatar = Column(String(100), default='https://res.cloudinary.com/dt1pa28g2/image/upload/v1765801014/default_avatar_dht_fu4l1b.jpg')
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    patients = relationship("Patient", backref="user", lazy=True)


    def __str__(self):
        return self.name


class Patient(BaseModel):
    __tablename__ = 'patient'
    name = Column(String(50), nullable=False)
    phone = Column(String(10), nullable=False)
    birthday = Column(DATE, nullable=False)
    address = Column(String(255), nullable=False)
    medical_history = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    appointment_schedules = relationship("AppointmentSchedule", backref="patient", lazy=True)


class Doctor(BaseModel):
    __tablename__ = 'doctor'
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    major = Column(String(100), nullable=True)
    appointment_schedules = relationship("AppointmentSchedule", backref="doctor", lazy=True)


class Service(BaseModel):
    __tablename__ = 'service'
    name = Column(String(100), nullable=False)
    price = Column(Double, nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    image = Column(String(200), default='https://res.cloudinary.com/dt1pa28g2/image/upload/v1765882079/service_default_ymbsdi.jpg')
    appointment_schedule_services = relationship("AppointmentScheduleService", backref="service", lazy=True)

    def __str__(self):
        return self.name


class Medicine(BaseModel):
    __tablename__ = 'medicine'
    name = Column(String(100), nullable=False)
    price = Column(Double, nullable=False)
    production_date = Column(DATE, nullable=False)
    expiration_date = Column(DATE, nullable=False)
    appointment_schedule_medicines = relationship("AppointmentScheduleMedicine", backref="medicine", lazy=True)

    def __str__(self):
        return self.name


class AppointmentSchedule(db.Model):
    __tablename__ = 'appointment_schedule'
    id = Column(Integer, primary_key=True, autoincrement=True)
    doctor_id = Column(Integer, ForeignKey("doctor.id"))
    patient_id = Column(Integer, ForeignKey("patient.id"))

    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(Enum(Status), default=Status.PENDING)

    invoice = relationship("Invoice", backref="appointment_schedule", lazy=True, uselist=False)
    treatment_card = relationship("TreatmentCard", backref="appointment_schedule", lazy=True, uselist=False)

    appointment_schedule_services = relationship("AppointmentScheduleService", backref="appointment_schedule",
                                                 lazy=True)
    appointment_schedule_medicines = relationship("AppointmentScheduleMedicine", backref="appointment_schedule",
                                                  lazy=True)

    __table_args__ = (
        UniqueConstraint('doctor_id', 'start_time'),
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

def insert_services():
    services = [
        {
            "name": "Bọc răng sứ",
            "price": 300000,
            "image": "https://res.cloudinary.com/dt1pa28g2/image/upload/v1765900829/icon-service-boc-rang-su_cpwtul.webp"
        },
        {
            "name": "Cấy ghép implant",
            "price": 500000,
            "image": "https://res.cloudinary.com/dt1pa28g2/image/upload/v1765900958/icon-service-implant_d1wvzp.webp"
        },
        {
            "name": "Niềng răng thẩm mỹ",
            "price": 1200000,
            "image": "https://res.cloudinary.com/dt1pa28g2/image/upload/v1765901070/icon-service-nieng-rang_d2swzn.png"
        },
        {
            "name": "Mặt dán sứ Veneer",
            "price": 5200000,
            "image": "https://res.cloudinary.com/dt1pa28g2/image/upload/v1765901120/icon-service-veneer_nxeebx.png"
        },
        {
            "name": "Tẩy trắng răng",
            "price": 3200000,
            "image": "https://res.cloudinary.com/dt1pa28g2/image/upload/v1765901187/icon-service-tay-trang-rang_hchtln.png"
        },
        {
            "name": "Nhổ răng khôn",
            "price": 100000,
            "image": "https://res.cloudinary.com/dt1pa28g2/image/upload/v1765901227/icon-service-nho-rang_ki3atr.png"
        },
        {
            "name": "Bệnh lý nha chu",
            "price": 100000,
            "image": "https://res.cloudinary.com/dt1pa28g2/image/upload/v1765901281/icon-service-dieu-tri-nha-chu_ck2ojw.png"
        },
        {
            "name": "Điều trị tuỷ",
            "price": 150000,
            "image": "https://res.cloudinary.com/dt1pa28g2/image/upload/v1765901322/icon-service-dieu-tri-tuy_n57ifs.png"
        },
        {
            "name": "Hàn trám răng",
            "price": 200000,
            "image": "https://res.cloudinary.com/dt1pa28g2/image/upload/v1765901368/icon-service-han-tram-rang_ada0bp.png"
        },
        {
            "name": "Cạo vôi răng",
            "price": 750000,
            "image": "https://res.cloudinary.com/dt1pa28g2/image/upload/v1765901419/icon-service-cao-voi-rang_zu7aym.png"
        },
        {
            "name": "Chăm sóc răng miệng cho thai phụ",
            "price": 1000000,
            "image": "https://res.cloudinary.com/dt1pa28g2/image/upload/v1765901475/icon-service-rang-mieng-thai-phu_csfkwv.png"
        },
        {
            "name": "Nha khoa trẻ em",
            "price": 1500000,
            "image": "https://res.cloudinary.com/dt1pa28g2/image/upload/v1765901521/icon-service-nha-khoa-tre-em_vgqcyr.png"
        }
    ]
    with app.app_context():
        for s in services:
            db.session.add(Service(**s))
        db.session.commit()

def insert_medicines():
    medicines = [
        {
            "name": "Paracetamol 500mg",
            "price": 15000,
            "production_date": "2025-01-10",
            "expiration_date": "2026-01-10"
        },
        {
            "name": "Amoxicillin 500mg",
            "price": 25000,
            "production_date": "2025-08-01",
            "expiration_date": "2026-08-01"
        },
        {
            "name": "Vitamin C",
            "price": 10000,
            "production_date": "2025-03-15",
            "expiration_date": "2027-03-15"
        },
        {
            "name": "paracetamol 500mg",
            "price": 25000,
            "production_date": "2025-08-01",
            "expiration_date": "2026-08-01"
        },
        {
            "name": "Benzocain 250mg",
            "price": 200000,
            "production_date": "2025-01-01",
            "expiration_date": "2025-08-01"
        },
        {
            "name": "Acetaminophen 500mg",
            "price": 15000,
            "production_date": "2025-01-01",
            "expiration_date": "2027-01-01"
        },
        {
            "name": "Thuốc kháng viêm 500mg",
            "price": 50000,
            "production_date": "2025-01-01",
            "expiration_date": "2026-01-01"
        }
    ]
    with app.app_context():
        for m in medicines:
            db.session.add(Medicine(**m))
        db.session.commit()



def create_user_base(name, phone, username, password, role):
    password = hash_password(password)
    user = User(name=name, phone=phone, username=username,password=password, user_role=role)
    db.session.add(user)
    db.session.flush()
    return user

def insert_doctors(count):
    majors = ["Chỉnh nha", "Phục hình", "Nha chu", "Implant", "Niềng", "Phẫu thuật tuỷ"]
    first_name = ["Hoàng", "Việt", "Minh", "Phúc", "Phát", "Việt"]
    last_name = ["Nguyễn", "Trần", "Phạm", "Ngô", "Lê"]
    with app.app_context():
        for i in range(1, count + 1):
            u = create_user_base(name=f"{random.choice(last_name)} {random.choice(first_name)}", phone=f"0912000{i:03d}", username=f"doctor{i}", password="123", role=UserRole.DOCTOR)
            dr = Doctor(id=u.id, major=random.choice(majors))
            db.session.add(dr)
        db.session.commit()


def insert_patient(count):
    first_name = ["Dung", "Nam", "Hậu", "Thành", "Trung", "Hoà"]
    last_name = ["Lý", "Tô", "Đặng", "Bùi", "Dương"]
    medical_history = ["Đau răng", "Đau lợi", "Chảy máu răng", "Sâu răng", "Rối loạn mọc răng"]
    with app.app_context():
        for i in range(1, count + 1):
            u = create_user_base(f"{random.choice(last_name)} {random.choice(first_name)}", f"0988000{i:03d}", f"user{i}", "123", UserRole.USER)
            pa = Patient(name=f"Bệnh nhân {random.choice(last_name)} {random.choice(first_name)}",phone=f"0988000{i:03d}",birthday=date(2000, 1, 1),address=f"Địa chỉ mẫu số {i}, TP.HCM", medical_history=random.choice(medical_history),user_id=u.id)
            db.session.add(pa)
        db.session.commit()


def init_all_data():
    with app.app_context():
        db.drop_all()
        db.create_all()

    insert_services()
    insert_medicines()
    with app.app_context():
        create_user_base("Nguyễn Văn Tuấn", "0334903055", "admin", "123", UserRole.ADMIN)
        db.session.commit()
    insert_doctors(4)
    insert_patient(10)

def create_slots(date):
    start_morning = datetime.combine(date, time(7, 0))
    end_morning = datetime.combine(date, time(11, 30))
    start_afternoon = datetime.combine(date, time(13, 0))
    end_afternoon = datetime.combine(date, time(16, 30))
    slots = []
    while start_morning <= end_morning:
        slots.append(start_morning)
        start_morning += timedelta(minutes=30)
    while start_afternoon <= end_afternoon:
        slots.append(start_afternoon)
        start_afternoon += timedelta(minutes=30)
    return slots


if __name__ == "__main__":
    init_all_data()
    # slots = create_slots(date.today())
    # for slot in slots:
    #     print(slot)