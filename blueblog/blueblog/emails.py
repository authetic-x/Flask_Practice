from flask import url_for, current_app
from flask_mail import Mail, Message
from blueblog.extensions import mail

def send_mail(subject, to, html):

    message = Message(subject, recipients=[to], body=html)
    mail.send(message)

def send_new_commment_email(post):

    post_url = url_for('blog.show_post', post_id=post.id, _external=True) + '#comments'
    send_mail(subject='New comment', to=current_app.config['BLUEBLOG_EMAIL'],
              html='<p>New Comment in post<i>%s</i>, click the link below to check:</p>'
                   '<p><a href="%s">%s</a></p>'
                   '<p><small style="color:#868e96">Do not reply this email.</small></p>'
                   % (post.title, post_url, post_url))

def send_new_reply_email(commment):

    post_url = url_for('blog.show_post', post_id=commment.id, _external=True) + '#comments'
    send_mail(subject='New reply', to=commment.email,
              html='<p>New reply for the comment you left in post<i>%s</i>, click the link below to check:</p>'
                   '<p><a href="%s">%s</a></p>'
                   '<p><small style="color:#868e96">Do not reply this email.</small></p>'
                   % (commment.post.title, post_url, post_url))