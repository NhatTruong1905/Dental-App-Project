from flask import render_template, Blueprint, request
from dentalapp.dao.services import load_services

services_bp = Blueprint('services', __name__)

@services_bp.route('/services')
def services_view():
    services = load_services(kw=request.args.get("kw"))
    return render_template("services.html", services=services)


