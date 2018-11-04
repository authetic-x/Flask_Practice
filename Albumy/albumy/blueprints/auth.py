
from flask import render_template, Blueprint, url_for, redirect, flash
from flask_login import login_required, login_user, logout_user, current_user, login_fresh, confirm_login

from albumy.settings import Operations
from albumy.emails import send_confirm_email, send_reset_password_email
from albumy.extensions import db
from albumy.models import User
from albumy.forms.auth import RegisterForm
from albumy.utils import generate_token


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data.lower()
        username = form.username.data
        password = form.password.data
        user = User(name=name, email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        token = generate_token(user=user, operation=Operations.CONFIRM)
        send_confirm_email(user=user, token=token)
        flash('Conform email sent, check your inbox.', 'info')
        return redirect(url_for('.login'))
    return render_template('auth/register.html', form=form)