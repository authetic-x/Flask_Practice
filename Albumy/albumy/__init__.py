
import os

import click
from flask import Flask
from flask_login import current_user
from flask_wtf.csrf import CSRFError

from albumy.blueprints.auth import auth_bp
from albumy.blueprints.main import main_bp
from albumy.blueprints.user import user_bp
from albumy.blueprints.ajax import ajax_bp
from albumy.extensions import db, moment, csrf, bootstrap, login_manager, mail,\
                dropzone, avatars, whooshee
from albumy.settings import config
from albumy.models import User, Role, Notification


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('albumy')

    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_shell_context(app)
    #register_template_context(app)
    register_errorhandlers(app)
    register_commands(app)

    return app


def register_extensions(app):
    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    dropzone.init_app(app)
    avatars.init_app(app)
    whooshee.init_app(app)

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(ajax_bp, url_prefix='/ajax')

def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        if current_user.is_authenticated:
            notification_count = Notification.query.with_parent(current_user).filter_by(is_read=False).count()
        else:
            notification_count = None
        return dict(notification_count=notification_count)


def register_errorhandlers(app):
    pass

def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='create after drop')
    def initdb(drop):
        '''Initialize the database'''
        if drop:
            click.confirm('The operation will delete the database, '
                          'will you like to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized the database.')

    @app.cli.command()
    def init():
        """Initialize the Albumy"""
        click.echo('Initializing the database...')
        db.create_all()

        click.echo('Initializing the roles and permissions...')
        Role.init_role()

        click.echo('Done.')

    @app.cli.command()
    @click.option('--user', default=10, help='Quantity of users, the default is 10.')
    def forge(user):
        """Generate fake data."""



        db.drop_all()
        db.create_all()

