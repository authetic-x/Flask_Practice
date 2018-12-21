import os

import click
from flask import Flask

from todoism.settings import config
from todoism.blueprints.todo import todo_bp
from todoism.blueprints.auth import auth_bp
from todoism.blueprints.home import home_bp
from todoism.extensions import db, login_manager


def create_app(config_name = None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('todoism')
    app.config.from_object(config[config_name])

    register_blueprints(app)
    register_extensions(app)
    register_commands(app)

    return app

def register_blueprints(app):
    app.register_blueprint(todo_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)

def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=False, help='create after drop')
    def initdb(drop):
        if drop:
            pass
        db.create_all()
        click.echo('Initialized database.')