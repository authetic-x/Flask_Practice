from threading import Thread

from flask import current_app, render_template
from flask_mail import Message

from albumy.extensions import mail


def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)

def send_mail(to, subject, template, **kwargs):
    pass

def send_confirm_email(user, token, to=None):
    pass

def send_reset_password_email(user, token):
    pass