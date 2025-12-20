from flask import jsonify, Blueprint
from flask_login import login_required, current_user
from dentalapp.dao import patients

api_patient_bp = Blueprint('patients', __name__)

@api_patient_bp.route('/api/patients/<int:id>', methods=["DELETE"])
@login_required
def delete_patient(id):
    try:
        if current_user.id != patients.get_patient(id).user.id:
            return jsonify({"ok": False, "message": "Patient not found!"})

        patients.delete_soft_patient(id)
        return jsonify({"ok": True, "message": "Patient deleted successfully!"})
    except Exception as e:
        return jsonify({"ok": False, "message": str(e)})

@api_patient_bp.route('/api/patients/<int:id>', methods=["PUT"])
@login_required
def edit_patient(id):
    try:
        if current_user.id != patients.get_patient(id).user.id:
            return jsonify({"ok": False, "message": "Patient not found!"})

        patient = patients.get_patient(id)
    except Exception as ex:
        return jsonify({"ok": False, "message": str(ex)})