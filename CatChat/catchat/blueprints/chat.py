from flask import Blueprint, render_template
from flask_login import current_user
from flask_socketio import emit

from catchat.extensions import socketio, db
from catchat.models import Message


chat_bp = Blueprint('chat', __name__)

online_users = []

@socketio.on('new message')
def new_message(message_body):
    message = Message(author=current_user._get_current_object(),
                      body=message_body)
    db.session.add(message)
    db.session.commit()
    emit('new message',
         {'message_html':render_template('', message=message)},
         broadcast=True)

@socketio.on('new message', namespace='/anonymous')
def new_anonymous_message(message_body):
    avatar = 'https://www.gravatar.com/avatar?d=mm'
    nickname = 'Anonymous'
    emit('new message',
         {'message_html': render_template('chat/_anonymous_message.html',
                                          message=message_body,
                                          avatar=avatar,
                                          nickname=nickname),
          'message_body': message_body,
          'gravatar': avatar,
          'nickname': nickname,
          'user_id': current_user.id},
         broadcast=True, namespace='/anonymous')

@chat_bp.route('/anonymous')
def anonymous():
    return render_template('chat/anonymous.html')

@socketio.on('connect')
def connect():
    global online_users
    if current_user.is_authenticated and current_user.id not in online_users:
        online_users.append(current_user.id)
    emit('user count', {'count':len(online_users)}, broadcast=True)

@socketio.on('disconnect')
def disconnect():
    global online_users
    if current_user.is_authenticated and current_user.id in online_users:
        online_users.remove(current_user.id)
    emit('user count', {'count':len(online_users)}, broadcast=True)