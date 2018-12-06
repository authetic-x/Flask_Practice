import os

import click
from flask import Flask
from flask_login import current_user

from todoism.blueprints.home import home_bp
from todoism.blueprints.auth import auth_bp
from todoism.blueprints.todo import todo_bp
from todoism.extensions import babel, db, login_manager, csrf
from todoism.settings import config
from todoism.models import Item


def create_app(config_name=None):

    if config_name == None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('todoism')
    app.config.from_object(config[config_name])

    register_blueprints(app)
    register_extensions(app)

    return app

def register_blueprints(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(todo_bp)

def register_extensions(app):
    babel.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

def register_template_context(app):
    @app.context_processor
    def make_template_context():
        if current_user.is_authenticated:
            active_items = Item.query.with_parent(current_user).filter_by(done=False).count()
        else:
            active_items = None
        return dict(active_items=active_items)

def register_error(app):
    pass

def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        if drop:
            click.confirm('are you sure?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')