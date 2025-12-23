from flask import Blueprint, render_template

from dentalapp.models import UserRole
from dentalapp.utils import permission

invoice_bp = Blueprint('invoice', __name__)


@invoice_bp.route('/invoice')
@permission({
    'roles': [UserRole.STAFF],
    'access': True
})
def render_invoice():
    return render_template('invoice.html')
