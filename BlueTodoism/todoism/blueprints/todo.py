
from flask import Blueprint, render_template, url_for, request, jsonify
from flask_login import login_required, current_user

from todoism.models import Item
from todoism.extensions import db

todo_bp = Blueprint('todo', __name__)


@todo_bp.route('/app')
@login_required
def app():
    all_count = Item.query.with_parent(current_user).count()
    active_count = Item.query.with_parent(current_user).filter_by(done=False).count()
    completed_count = Item.query.with_parent(current_user).filter_by(done=True).count()
    return render_template('_app.html', items=current_user.items, all_count=all_count,
                           active_count=active_count, completed_count=completed_count)

@todo_bp.route('/items/new', methods=['GET', 'POST'])
@login_required
def new_item():
    data = request.get_json()
    if data is None or data['body'].strip() == '':
        jsonify(message='Invalid item body.'), 400
    item = Item(body=data['body'], author=current_user._get_current_object())
    db.session.add(item)
    db.session.commit()
    return jsonify(html=render_template('_item.html', item=item), message='+1')

@todo_bp.route('/items/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    pass

@todo_bp.route('/items/<int:item_id>/toggle', methods=['PATCH'])
@login_required
def toggle_item(item_id):
    item = Item.query.get_or_404(item_id)
    item.done = not item.done
    db.session.commit()
    return jsonify(message='Item toggled.')

@todo_bp.route('/item/new')
@login_required
def clear():
    pass