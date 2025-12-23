from dentalapp.models import Doctor, User, UserRole
from sqlalchemy import and_
from dentalapp import app


def load_doctors(kw=None, page=1):
    query = Doctor.query
    if kw:
        query = query.join(User, User.id==Doctor.id).filter(User.name.contains(kw))

    start = (page - 1) * app.config['PAGE_SIZE']
    query = query.slice(start, start + app.config['PAGE_SIZE'])
    return query.all()


def get_infor_doctor(doctor_id):
    return Doctor.query.get(doctor_id)

def count_doctors():
    return Doctor.query.count()
