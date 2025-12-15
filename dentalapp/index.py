from dentalapp.routes import home
from dentalapp import app, login
from dao import user

@login.user_loader
def load_user(user_id):
    return user.get_current_user(user_id)

if __name__ == '__main__':
    app.register_blueprint(home.home_bp)


    app.run(debug=True)

