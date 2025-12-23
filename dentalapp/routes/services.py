from flask import render_template, Blueprint, request
from dentalapp.dao.services import load_services, count_services

services_bp = Blueprint('services', __name__)

@services_bp.route('/services')
def services_view():
    services = [service for service in load_services(kw=request.args.get("kw"), page=int(request.args.get("page", 1))) if service.active]
    count = count_services()
    return render_template("services.html", services=services, count=count)


