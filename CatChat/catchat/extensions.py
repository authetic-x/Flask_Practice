from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_moment import Moment
from flask_oauthlib.client import OAuth


db = SQLAlchemy()
socketio = SocketIO()
moment = Moment()
oauth = OAuth()