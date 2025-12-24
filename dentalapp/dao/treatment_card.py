from dentalapp import app, db
from dentalapp.models import TreatmentCard


def save_treatment_card(appointment_schedule_id, note):
    treatment_card = TreatmentCard(appointment_schedule_id=appointment_schedule_id, note=note)
    db.session.add(treatment_card)