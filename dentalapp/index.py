from dentalapp.routes import home, login_logout, register, change_password
from dentalapp import app, login
from dentalapp.dao import users
from dentalapp.admin import *



@login.user_loader
def load_user(user_id):
    return users.get_current_user(user_id)


if __name__ == '__main__':
    app.register_blueprint(home.home_bp)
    app.register_blueprint(login_logout.login_logout_bp)
    app.register_blueprint(register.register_bp)
    app.register_blueprint(change_password.change_password_bp)

    app.run(debug=True)
