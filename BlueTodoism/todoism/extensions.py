
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please login to access this page.'

@login_manager.user_loader
def load_user(userid):
    from todoism.models import User
    return User.query.get(int(userid))