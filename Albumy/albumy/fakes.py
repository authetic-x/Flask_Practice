import os
import random

from faker import Faker
from sqlalchemy.exc import IntegrityError
from flask import current_app
from PIL import Image

from albumy.models import User, Notification, Tag, Photo, Comment
from albumy.extensions import db

fake = Faker()


def fake_admin():
    admin = User(
        name = 'Hong Zhe',
        username = 'authetic',
        email = '1019892846@qq.com',
        bio = fake.sentence(),
        confirmed = True,
        website = 'https://github.com/authetic-x'
    )
    admin.set_password('123456')
    notification = Notification(message='Welcome to Albumy!', receiver=admin)
    db.session.add(admin)
    db.session.add(notification)
    db.session.commit()

def fake_user(count=10):
    for i in range(count):
        user = User(
            name = fake.name(),
            username = fake.user_name(),
            confirmed = True,
            bio = fake.sentence(),
            location = fake.city(),
            website = fake.url(),
            member_since = fake.date_this_decade(),
            email = fake.email()
        )
        user.set_password('123456')
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

def fake_follow(count=30):
    for i in range(count):
        user = User.query.get(random.randint(1, User.query.count()))
        user.follow(User.query.get(random.randint(1, User.query.count())))
        user.follow(User.query.filter_by(username='authetic').first())
    db.session.commit()

def fake_tag(count=20):
    for i in range(count):
        tag = Tag(name=fake.word())
        db.session.add(tag)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

def fake_photo(count=30):
    upload_path = current_app.config['ALBUMY_UPLOAD_PATH']
    for i in range(count):
        print('synthesise photo', i)

        filename = 'random_%d.jpg' % i
        r = lambda : random.randint(128, 255)
        image = Image.new(mode='RGB', size=(800,800), color=(r(), r(), r()))
        image.save(os.path.join(upload_path, filename))

        photo = Photo(
            description=fake.text(),
            timestamp=fake.date_time_this_year(),
            author=User.query.get(random.randint(1, User.query.count())),
            filename=filename,
            filename_m=filename,
            filename_s=filename
        )
        for j in range(random.randint(1, 5)):
            tag = Tag.query.get(random.randint(1, Tag.query.count()))
            if tag not in photo.tags:
                photo.tags.append(tag)
        db.session.add(photo)
    db.session.commit()

def fake_collect(count=30):
    for i in range(count):
        user = User.query.get(random.randint(1, User.query.count()))
        user.collect(Photo.query.get(random.randint(1, Photo.query.count())))
    db.session.commit()

def fake_comment(count=30):
    for i in range(count):
        comment = Comment(
            author=User.query.get(random.randint(1, User.query.count())),
            body = fake.sentence(),
            timestamp=fake.date_time_this_year(),
            photo=Photo.query.get(random.randint(1, Photo.query.count()))
        )
        db.session.add(comment)
    db.session.commit()