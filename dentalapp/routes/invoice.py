from flask import Blueprint, render_template

invoice_bp = Blueprint('invoice', __name__)


@invoice_bp.route('/invoice')
def render_invoice():
    return render_template('invoice.html')
