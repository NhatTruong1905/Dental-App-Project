from dentalapp.models import Medicine
from datetime import date


def load_medicines():
    return Medicine.query.filter((Medicine.expiration_date >= date.today()) & (Medicine.active == True)).all()
