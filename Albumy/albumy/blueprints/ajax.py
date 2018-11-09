from flask import Blueprint, render_template, jsonify
from flask_login import current_user

from albumy.models import User, Notification



ajax_bp = Blueprint('ajax', __name__)


@ajax_bp.route('/profile/<int:user_id')
def get_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('main/profile_popup.html', user=user)

@ajax_bp.route('/notification-count')
def notifications_count():
    if not current_user.is_authenticated:
        return jsonify(message='Login required.'), 403

    count = Notification.query.with_parent(current_user).filter_by(is_read=False).count()
    return jsonify(count=count)