#coding: utf-8

import os

from flask import url_for, render_template, redirect, Blueprint, request, \
                    current_app, send_from_directory, flash, abort
from flask_login import login_required, current_user
from flask_dropzone import random_filename

from albumy.decorators import confirm_required, permission_required, admin_required
from albumy.models import Photo
from albumy.extensions import db
from albumy.utils import resize_image, flash_errors
from albumy.forms.main import DescriptionForm


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

@main_bp.route('/avatars/<path:filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'], filename)

@main_bp.route('/uploads/<path:filename>')
def get_image(filename):
    return send_from_directory(current_app.config['ALBUMY_UPLOAD_PATH'], filename)

@main_bp.route('/photo<int:photo_id>')
def show_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    description_form = DescriptionForm()
    description_form.description.data = photo.description
    return render_template('main/photo.html', photo=photo, description_form=description_form)

@main_bp.route('/photo/n/<int:photo_id>')
def photo_next(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    photo_n = Photo.query.with_parent(photo.author).filter(Photo.id > photo_id).order_by(
                        Photo.id.asc()).first()
    if photo_n is None:
        flash('This is already the last one.', 'info')
        return redirect(url_for('.show_photo', photo_id=photo_id))
    return redirect(url_for('.show_photo', photo_id=photo_n.id))

@main_bp.route('/photo/p/<int:photo_id>')
def photo_previous(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    photo_p = Photo.query.with_parent(photo.author).filter(Photo.id < photo_id)\
                    .order_by(Photo.id.desc()).first()
    if photo_p is None:
        flash('This is already first one.', 'info')
        return redirect(url_for('.show_photo', photo_id=photo_id))
    return redirect(url_for('.show_photo', photo_id=photo_p.id))

@main_bp.route('/delete/photo/<int:photo_id>')
@login_required
def delete_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    if current_user != photo.author:
        abort(403)

    db.session.delete(photo)
    db.session.commit()
    flash('Photo deleted.', 'info')

    photo_n = Photo.query.with_parent(photo.author).filter(Photo.id < photo_id).\
                            order_by(Photo.id.desc()).first()
    if photo_n is None:
        photo_p = Photo.query.with_parent(photo.author).filter(Photo.id > photo_id).\
                            order_by(Photo.id.asc()).first()
        if photo_p is None:
            return redirect(url_for('user.index', username=photo.author.username))
        return redirect(url_for('.show_photo', photo_id=photo_p.id))
    return redirect(url_for('.show_photo', photo_id=photo.n.id))

@main_bp.route('/report/photo/<int:photo_id>', methods=['POST'])
@login_required
@confirm_required
def report_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    photo.flag += 1
    db.session.commit()
    flash('Photo reported', 'success')
    return redirect(url_for('.show_photo', photo_id=photo.id))

@main_bp.route('/photo/<int:photo_id>/description', methods=['POST'])
@login_required
def edit_description(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    if current_user != photo.author:
        abort(403)

    form = DescriptionForm()
    if form.validate_on_submit():
        photo.description = form.description.data
        db.session.commit()
        flash('Description updated.', 'success')
        flash_errors(form)
        return redirect(url_for('.show_post', photo_id=photo_id))