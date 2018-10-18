from flask import Flask, render_template, flash, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
import click
from forms import NewNoteForm, EditNoteForm, DeleteNoteForm

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret string')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 'sqlite:///' + os.path.join(app.root_path, 'data.db')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/')
def index():
    form = DeleteNoteForm()
    notes = Note.query.all()
    return render_template('index.html', notes=notes, form=form)

@app.route('/new', methods=['GET', 'POST'])
def new_node():
    form = NewNoteForm()

    if form.validate_on_submit():
        body = form.body.data
        note = Note(body=body)
        db.session.add(note)
        db.session.commit()
        flash('Your note is saved')
        return redirect(url_for('index'))
    return render_template('new_note.html', form=form)

@app.route('/edit<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    form  = EditNoteForm()
    note = Note.query.get(note_id)

    if form.validate_on_submit():
        note.body = form.body.data
        db.session.commit()
        flash('Your note is updated')
        return redirect(url_for('index'))
    form.body.data = note.body
    return render_template('edit_note.html', form=form)

@app.route('/delete/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    form = DeleteNoteForm()
    if form.validate_on_submit():
        note = Note.query.get(note_id)
        db.session.delete(note)
        db.session.commit()
        flash('Your note is deleted')
    else:
        abort(400)
    return redirect(url_for('index'))


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)

@app.cli.command()
def initdb():
    db.create_all()
    click.echo('Initialized database')


if __name__ == '__main__':
    app.run()
