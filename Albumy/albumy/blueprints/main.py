#coding: utf-8

import os

from flask import url_for, render_template, redirect, Blueprint, request
from flask_login import login_required

from albumy.decorators import confirm_required, permission_required, admin_required


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('macros.html')

@main_bp.route('/upload', methods=['GTE', 'POST'])
@login_required
@confirm_required
@permission_required('UPLOAD')
def upload():
    if request.method == 'POST' and 'file' in request.files:
