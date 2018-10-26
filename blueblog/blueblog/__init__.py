from flask import Flask, render_template
from blueblog.settings import config
from blueblog.extensions import bootstrap, db, moment, ckeditor,\
    mail, login_manager, csrf
from blueblog.models import Admin, Category, Comment
from blueblog.blueprints.blog import blog_bp
from blueblog.blueprints.auth import auth_bp
from blueblog.blueprints.admin import admin_bp
from flask_wtf.csrf import CSRFError
from flask_login import current_user

import os
import click


def create_app(config_name=None):

    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('blueblog')
    app.config.from_object(config[config_name])

    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errors(app)
    register_shell_context(app)
    register_template_context(app)

    return app

def register_logging(app):
    pass

def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(auth_bp, prefix='auth')
    app.register_blueprint(admin_bp, prefix='admin')

def register_shell_context(app):

    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)

def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments = None
        return dict(admin=admin, categories=categories,
                    unread_comments=unread_comments)

def register_errors(app):

    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html')

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 400

def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop')
    def initdb(drop):
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories, default is 10')
    @click.option('--post', default=50, help='Quantity of posts, default is 50')
    @click.option('--comment', default=500, help='Quantity of comments, default is 500')
    def forge(category, post, comment):
        from blueblog.fakes import fake_admin, fake_categories, fake_comments, fake_posts

        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()

        click.echo('Generating %d categories...' % category)
        fake_categories(category)

        click.echo('Generating %d posts...' % post)
        fake_posts(post)

        click.echo('Generating %d comments...' % comment)
        fake_comments(comment)

        click.echo('Done')

    @app.cli.command()
    def query():
        from blueblog.models import Admin
        print(Admin.query.filter_by(id=1))

    @app.cli.command()
    @click.option('--username', prompt=True, help='The userName used to login')
    @click.option('--password', prompt=True, hide_input=False, confirmation_prompt
                  =True, help='The password used to login')
    def init(username, password):
        click.echo('Initializing the database...')
        db.create_all()

        admin = Admin.query.first()
        if admin:
            click.echo('The administrator already exist, updating...')
            admin.username = username
            admin.set_password(password)
        else:
            click.echo('Creating temporary administrator account...')
            admin = Admin(
                username = username,
                blog_title='Blueblog',
                blog_sub_title="I love ZAYN MALIK",
                name = 'Admin',
                about='Anything about you'
            )
            admin.set_password(password)
            db.session.add(admin)

        category = Category.query.first()
        if category is None:
            click.echo('Creating the default category...')
            category = Category(name='Default')
            db.session.add(category)

        db.session.commit()
        click.echo('Done.')