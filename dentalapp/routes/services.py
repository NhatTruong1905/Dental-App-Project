from flask import render_template, Blueprint, request

from dentalapp import app
from dentalapp.dao.services import load_services, count_services
import math

services_bp = Blueprint('services', __name__)

@services_bp.route('/services')
def services_view():
    services = [service for service in load_services(kw=request.args.get("kw"), page=int(request.args.get("page", 1))) if service.active]
    pages = math.ceil(count_services() / app.config['PAGE_SIZE'])
    return render_template("services.html", services=services, pages=pages)


