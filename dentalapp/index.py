from dentalapp import app, login
from flask import render_template
from dentalapp.admin import *
from dentalapp.dao import get_current_user


@app.route('/')
def home():
    return render_template('index.html')

@login.user_loader
def load_user(user_id):
    return get_current_user(user_id)


if __name__ == '__main__':
    app.run(debug=True)