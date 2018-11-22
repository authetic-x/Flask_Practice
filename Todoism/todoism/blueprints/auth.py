from flask import Blueprint, jsonify
from faker import Faker

from todoism.models import User, Item
from todoism.extensions import db


auth_bp = Blueprint('auth', __name__)
fake = Faker()

@auth_bp.route('/register')
def register():
    username = fake.user_name()
    while User.query.filter_by(username=username).first() is not None:
        username = fake.user_name()
    password = fake.word()
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    item1 = Item(body = fake.word(), author=user)
    item2 = Item(body=fake.word(), author=user)
    item3 = Item(body=fake.word(), author=user)
    item4 = Item(body=fake.word(), done=True, author=user)
    db.session.add_all([item1, item2, item3, item4])
    db.session.commit()
    return jsonify(username=username, password=password, message='Generate success.')