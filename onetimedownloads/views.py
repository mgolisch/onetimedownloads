from flask import render_template, url_for, redirect, session, flash
from onetimedownloads import app, db
from onetimedownloads.forms import LoginForm
from onetimedownloads.models import User, File, Code
from functools import wraps


# helpers
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'userid' not in session:
            flash('not logged in')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


# views
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['get', 'post'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data,
                                    password=form.password.data).first()
        if user is not None:
            session['userid'] = user.id
            session['username'] = user.name
            flash('logged in')
            return redirect(url_for('index'))
        else:
            flash('invalid login', 'error')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    del session['userid']
    del session['username']
    flash('logged out')
    return redirect(url_for('index'))


@app.route('/files')
@login_required
def manage_files():
    userid = session['userid']
    user = User.query.get(userid)
    return render_template('files.html', files=user.files)


@app.route('/files/delete/<int:id>')
@login_required
def delete_file(fileid):
    pass


@app.route('/files/add')
@login_required
def add_file():
    pass
