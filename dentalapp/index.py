from dentalapp.routes import home, login_logout, register, change_password, services, patients, doctors, infor_user, \
    appointment, employees, invoice
from dentalapp.api import api_patients, api_doctors, api_users, api_services, api_appointment_schedule
from dentalapp import app, login
from dentalapp.admin import *


@login.user_loader
def load_user(user_id):
    return infor_user.get_current_user(user_id)


def register_routes():
    app.register_blueprint(home.home_bp)
    app.register_blueprint(login_logout.login_logout_bp)
    app.register_blueprint(register.register_bp)
    app.register_blueprint(change_password.change_password_bp)
    app.register_blueprint(services.services_bp)
    app.register_blueprint(patients.patient_bp)
    app.register_blueprint(doctors.doctors_bp)
    app.register_blueprint(infor_user.infor_user_bp)
    app.register_blueprint(appointment.appointment_bp)
    app.register_blueprint(employees.employees_bp)
    app.register_blueprint(invoice.invoice_bp)


def register_api():
    app.register_blueprint(api_patients.api_patient_bp)
    app.register_blueprint(api_users.api_users_bp)
    app.register_blueprint(api_doctors.api_doctors_bp)
    app.register_blueprint(api_services.api_services_bp)
    app.register_blueprint(api_appointment_schedule.api_appointment_schedule)


if __name__ == '__main__':
    register_routes()
    register_api()
    app.run(debug=True)
