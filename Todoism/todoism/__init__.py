from flask import Flask

from todoism.blueprints.home import home
from todoism.extensions import babel, db


def create_app():

    app = Flask('todoism')

    register_blueprints(app)
    register_extensions(app)

    return app

def register_blueprints(app):
    app.register_blueprint(home)

def register_extensions(app):
    babel.init_app(app)
    db.init_app(app)
