from flask import Flask

from todoism.blueprints.home import home


def create_app():

    app = Flask('todoism')

    register_blueprints(app)

    return app

def register_blueprints(app):
    app.register_blueprint(home)