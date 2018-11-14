from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import login_required

from albumy.decorators import permission_required, admin_required
from albumy.models import User, Role, Photo, Comment, Tag
from albumy.utils import redirect_back
from albumy.forms.admin import EditProfileAdminForm
from albumy.extensions import db


admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/')
@login_required
@permission_required('MODERATE')
def index():
    user_count = User.query.count()
    locked_user_count = User.query.filter_by(locked=True).count()
    blocked_user_count = User.query.filter_by(active=False).count()
    photo_count = Photo.query.count()
    reported_photos_count = Photo.query.filter(Photo.flag > 0).count()
    tag_count = Tag.query.count()
    comment_count = Comment.query.count()
    reported_comments_count = Comment.query.filter(Comment.flag > 0).count()
    return render_template('admin/index.html', user_count=user_count, photo_count=photo_count,
                           tag_count=tag_count, comment_count=comment_count, locked_user_count=locked_user_count,
                           blocked_user_count=blocked_user_count, reported_comments_count=reported_comments_count,
                           reported_photos_count=reported_photos_count)


@admin_bp.route('/lock/user/<int:user_id>', methods=['POST'])
@permission_required('MODERATE')
def lock_user(user_id):
    user = User.query.get_or_404(user_id)
    user.lock()
    flash('Account locked', 'info')
    return redirect_back()

@admin_bp.route('/unlock/user<int:user_id>', methods=['POST'])
@permission_required('MODERATE')
def unlock_user(user_id):
    user = User.query.get_or_404(user_id)
    user.unlock()
    flash('Lock canceled', 'info')
    return redirect_back()

@admin_bp.route('/profile/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_profile_admin(user_id):
    user = User.query.get_or_404(user_id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.name = form.name.data
        role = Role.query.get(form.role.data)
        if role.name == 'Locked':
            user.lock()
        user.role = role
        user.bio = form.bio.data
        user.website = form.website.data
        user.confirmed = form.confirmed.data
        user.active = form.active.data
        user.location = form.location.data
        user.username = form.username.data
        user.email = form.email.data
        db.session.commit()
        flash('Profile updated.', 'success')
        return redirect_back()
    form.name.data = user.name
    form.role.data = user.role_id
    form.bio.data = user.bio
    form.website.data = user.website
    form.location.data = user.location
    form.username.data = user.username
    form.email.data = user.email
    form.confirmed.data = user.confirmed
    form.active.data = user.active
    return render_template('admin/edit_profile.html', form=form, user=user)

@admin_bp.route('/delete/tag/<int:tag_id>')
@admin_required
def delete_tag(tag_id):
    pass
