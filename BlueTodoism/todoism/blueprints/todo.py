
from flask import Blueprint, render_template, url_for

todo_bp = Blueprint('todo', __name__)


@todo_bp.route('/')
def index():
    return render_template('index.html')