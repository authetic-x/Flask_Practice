import os

from flask import Blueprint

from catchat.extensions import oauth, db

oauth_bp = Blueprint('oauth', __name__)


github = oauth.remote_app(
    name='github',
    consumer_key = os.getenv('GITHUB_CLIENT_ID'),
    consumer_secert = os.getenv('GITHUB_CLIENT_SECRET'),
    request_token_params = {'scope':'user'},
    base_url = 'https://api.github.com/',
    request_token_url = None,
    access_token_method = 'POST',
    access_token_url = 'https://github.com/login/oauth/access_token',
    authorize_url = 'https://github.com/login/oauth/authorize'
)