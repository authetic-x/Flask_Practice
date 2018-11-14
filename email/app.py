from flask import Flask
from flask_mail import Mail

import os

app = Flask(__name__)

app.config.update(
    MAIL_SERVER = os.getenv('MAIL_SERVER'),
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USERNAME = os.getenv('MAIL_USRENAME'),
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER = ('Grey Li', os.getenv('MAIL_USERNAME'))
)

mail = Mail(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
