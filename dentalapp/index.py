from dentalapp.routes import home, login_logout
from dentalapp import app, login
from dao import users


@login.user_loader
def load_user(user_id):
    return users.get_current_user(user_id)


if __name__ == '__main__':
    app.register_blueprint(home.home_bp)
    app.register_blueprint(login_logout.home_bp)

    app.run(debug=True)
