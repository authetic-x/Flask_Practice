from flask import Flask, render_template, flash, redirect, url_for
from forms import LoginForm, UploadForm

app = Flask(__name__)
app.secret_key = 'secret_string'


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
        pass
    return render_template('')

if __name__ == '__main__':
    app.run()
