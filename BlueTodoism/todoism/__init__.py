import os

import click
from flask import Flask

from todoism.settings import config
from todoism.blueprints.todo import todo_bp


def create_app(config_name = None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('todoism')
    #app.config.from_object(config[config_name])

    register_blueprints(app)

    return app

def register_blueprints(app):
    app.register_blueprint(todo_bp)
