from dentalapp.models import Doctor


def load_doctors():
    return Doctor.query.all()


def get_infor_doctor(doctor_id):
    return Doctor.query.get(doctor_id)
