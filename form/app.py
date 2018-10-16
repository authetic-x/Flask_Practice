from flask import Flask, render_template, flash, redirect, url_for, \
    send_from_directory, session, request
from forms import LoginForm, UploadForm, MultiUploadForm, RichTextForm, \
    SigninForm, RegisterForm
from wtforms import ValidationError
from flask_wtf.csrf import validate_csrf
from flask_ckeditor import CKEditor

import os, uuid

app = Flask(__name__)
app.secret_key = 'secret_string'

app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')
app.config['ALLOW_EXTENSIONS'] = ['jpg', 'png', 'jpeg', 'gif']
app.config['CKEDITOR_SERVE_LOCAL'] = True

ckeditor = CKEditor(app)


@app.route('/')
def index():
    return render_template('base.html')

@app.route('/basic')
def basic():
    form = LoginForm()
    return render_template('basic.html', form=form)

@app.route('/bootstrap', methods=['GET', 'POST'])
def bootstrap():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        flash('Welcome home, %s!' % username)
        return redirect(url_for('index'))
    return render_template('bootstrap.html', form=form)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = random_file(f.filename)
        f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        flash('Upload success')
        session['filenames'] = filename
        return redirect(url_for('show_image'))
    return render_template('upload.html', form=form)

@app.route('/upload/<path:filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

@app.route('/upload-images')
def show_image():
    return render_template('uploaded.html')

def random_file(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.',1)[1].lower() in app.config['ALLOW_EXTENSIONS']

@app.route('/multi-upload', methods=['GET', 'POST'])
def multi_upload():
    form = MultiUploadForm()
    if request.method == 'POST':
        filenames = []
        try:
            validate_csrf(form.csrf_token.data)
        except ValidationError:
            flash('CSRF token error')
            return redirect(url_for('multi_upload'))
        if 'photo' not in request.files:
            flash('This field is required')
            return redirect(url_for('multi_upload'))
        for f in request.files.getlist('photo'):
            if f and allowed_file(f.filename):
                filename = random_file(f.filename)
                f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                filenames.append(filename)
            else:
                flash('Invalid file type.')
                return redirect(url_for('multi_upload'))
        flash('Upload Success.')
        session['filenames'] = filenames
        return redirect(url_for('show_image'))
    return render_template('upload.html', form=form)

@app.route('/ckeditor', methods=['GET', 'POST'])
def ckeditor():
    form = RichTextForm()
    return render_template('ckeditor.html', form=form)

@app.route('/multi-form', methods=['GET', 'POST'])
def multi_form():
    signin_form = SigninForm()
    register_form = RegisterForm()

    if signin_form.submit1.data and signin_form.validate():
        username = signin_form.username.data
        flash('%s, you just submit the signinForm' % username)
        return redirect(url_for('index'))
    if register_form.submit2.data and register_form.validate():
        username = register_form.username.data
        flash('%s, you just submit the RegisterForm' % username)
        return redirect(url_for('index'))
    return render_template('')

@app.route('/handle_signin', methods=['POST'])
def handle_signin():
    signin_form = SigninForm()
    register_form = RegisterForm()

    if signin_form.validate_on_submit():
        pass

if __name__ == '__main__':
    app.run()
