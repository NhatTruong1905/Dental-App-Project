from dentalapp.models import Service
from dentalapp import app


def load_services(kw=None, page=1):
    query = Service.query
    if kw:
        query = query.filter(Service.name.contains(kw))

    if page:
        start = (page - 1) * app.config['PAGE_SIZE']
        query = query.slice(start, start + app.config['PAGE_SIZE'])
    return query.all()

def count_services():
    return Service.query.count()
