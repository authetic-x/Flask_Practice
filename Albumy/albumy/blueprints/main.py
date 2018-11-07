#coding: utf-8

import os

from flask import url_for, render_template, redirect, Blueprint, request, \
                    current_app
from flask_login import login_required, current_user
from flask_dropzone import random_filename

from albumy.decorators import confirm_required, permission_required, admin_required
from albumy.models import Photo
from albumy.extensions import db
from albumy.utils import resize_image


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
        f = request.files.get('file')
        filename = random_filename(f.fileanme)
        f.save(os.path.join(current_app.config['ALBUMY_UPLOAD_PATH']), filename)
        filename_s = resize_image(f, filename, 400)
        filename_m = resize_image(f, filename, 800)
        photo =Photo(
            filename=filename,
            filename_s = filename_s,
            filename_m = filename_m,
            author=current_user._get_current_object()
        )
        db.session.add(photo)
        db.session.commit()
    return render_template('main/upload.html')