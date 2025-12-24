from dentalapp import db
from dentalapp.models import Invoice, AppointmentSchedule


def saveInvoice(appointment_id, total_service, total_medicine, vat, total_invoice):
    invoice = Invoice(appointment_schedule_id=appointment_id, total_service=total_service,
                      total_medicine=total_medicine, vat=vat, total_invoice=total_invoice)

    db.session.add(invoice)

    update_status_appointment_of_invoice(appointment_id)

    db.session.commit()


def update_status_appointment_of_invoice(appointment_id):
    try:
        db.session.query(AppointmentSchedule).filter(AppointmentSchedule.id == appointment_id).update(
            {AppointmentSchedule.status: "SUCCESS"})

        db.session.commit()
        return True
    except Exception as e:
        print(f"Lỗi: {e}")
        db.session.rollback()
        return False
