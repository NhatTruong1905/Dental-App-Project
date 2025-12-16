from dentalapp.models import Service


def load_services(kw=None, page=1):
    query = Service.query
    if kw:
        query = query.filter(Service.name.contains(kw))
    return query.all()
