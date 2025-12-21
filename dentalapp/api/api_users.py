from flask import Blueprint, jsonify, request
from dentalapp.utils import permission
from dentalapp.dao import users

api_users_bp = Blueprint('api_users', __name__)

@api_users_bp.route('/api/users/<int:id>', methods=['PUT'])
@permission()
def update_infor_users(id):
    try:
        name = request.form.get("name")
        phone = request.form.get("phone")
        avatar = request.files.get("avatar")
        users.update_user(id, name, phone, avatar)
        return jsonify({"ok": True, "message": "Update user successfully"})
    except Exception as ex:
        return jsonify({"ok": False, "error": str(ex)})
