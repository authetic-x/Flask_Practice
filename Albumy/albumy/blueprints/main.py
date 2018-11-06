#coding: utf-8

import os

from flask import url_for, render_template, redirect, Blueprint


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('macros.html')