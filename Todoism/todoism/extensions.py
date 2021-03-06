
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from flask_login import LoginManager, current_user
from flask_wtf.csrf import CSRFProtect


db = SQLAlchemy()
babel = Babel()
csrf = CSRFProtect()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please login to access this page'

@login_manager.user_loader
def load_user(user_id):
    from todoism.models import User
    return User.query.get(int(user_id))
