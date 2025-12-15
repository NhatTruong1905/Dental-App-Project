from dentalapp.models import Service


def load_services():
    return Service.query.all()
