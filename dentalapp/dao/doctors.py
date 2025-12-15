from dentalapp.models import Doctor


def load_doctors():
    return Doctor.query.all()
