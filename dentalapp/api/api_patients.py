from flask import jsonify, Blueprint
from flask_login import current_user
from dentalapp.dao.patients import get_patient, get_list_patients, delete_soft_patient
from dentalapp.models import UserRole
from dentalapp.utils import permission
from dentalapp.dao import appointment_schedules

api_patient_bp = Blueprint('patients', __name__)


@api_patient_bp.route('/api/patients/<int:id>', methods=["DELETE"])
@permission()
def delete_patient(id):
    try:
        if current_user.id != get_patient(id).user.id:
            return jsonify({"ok": False, "message": "Patient not found!"})

        delete_soft_patient(id)
        return jsonify({"ok": True, "message": "Patient deleted successfully!"})
    except Exception as e:
        return jsonify({"ok": False, "message": str(e)})


@api_patient_bp.route('/api/patients', methods=["GET"])
@permission()
def get_patients():
    if current_user.user_role in [UserRole.ADMIN, UserRole.STAFF]:
        patients = get_list_patients(full=True)
    else:
        patients = get_list_patients(full=False)
    patients = [
        {
            "id": patient.id,
            "name": patient.name
        }
        for patient in patients
    ]

    return jsonify(patients)


