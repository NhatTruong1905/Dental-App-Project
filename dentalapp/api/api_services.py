from flask import Blueprint, jsonify
from dentalapp.utils import permission
from dentalapp.dao.services import load_services

api_services_bp = Blueprint("api_services", __name__)

@api_services_bp.route("/api/services", methods=["GET"])
@permission()
def get_services():
    services = load_services(page=None)

    services_json = [
        {
            "id": service.id,
            "name": service.name,
            "price": service.price
        }
        for service in services if service.active
    ]

    return jsonify(services_json)