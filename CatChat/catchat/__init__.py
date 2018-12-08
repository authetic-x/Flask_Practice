import os

import click
from flask import Flask

from catchat.settings import config
from catchat.extensions import socketio, db, oauth


def create_app(config_name=None):

    if config_name == None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('catchat')
    app.config.from_object(config[config_name])
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)

    return app

def register_blueprints(app):
    pass

def register_extensions(app):
    db.init_app(app)
    socketio.init_app(app)
    oauth.init_app(app)

def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=False, help='')
    def initdb(drop):
        pass

    @app.cli.command()
    @click.option('--message', default=300, help='')
    def forge(message):
        pass