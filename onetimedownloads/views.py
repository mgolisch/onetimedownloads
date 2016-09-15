from flask import render_template, url_for, redirect, session, flash, request, send_file
from werkzeug.utils import secure_filename
from onetimedownloads import app, db
from onetimedownloads.forms import LoginForm, UploadForm, DownloadForm
from onetimedownloads.models import User, File, Code
from functools import wraps
from datetime import datetime
import io


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


@app.route('/files/delete/<int:fileid>')
@login_required
def delete_file(fileid):
    userid = session['userid']
    file = File.query.get(fileid)
    if file is None:
        flash('invalid fileid','error')
        return redirect(url_for('manage_files'))
    if not file.userid == userid:
        flash('file doesnt belong to you','error')
        return redirect(url_for('manage_files'))
    for code in file.codes:
        db.session.delete(code)
    db.session.delete(file)
    db.session.commit()
    flash('file deleted')
    return redirect(url_for('manage_files'))



@app.route('/files/add', methods=['get', 'post'])
@login_required
def add_file():
    userid = session['userid']
    user = User.query.get(userid)
    form = UploadForm()
    if form.validate_on_submit():
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        uploaded_file = request.files['file']
        if uploaded_file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        file = File()
        file.data = uploaded_file.read()
        file.filename = secure_filename(uploaded_file.filename)
        uploaded_file.seek(0,2)
        file.size = uploaded_file.tell()
        file.created_at = datetime.now()
        file.userid = userid
        db.session.add(file)
        db.session.commit()    
        flash('File uploaded')
        return redirect(url_for('manage_files'))
        
    return render_template('files_add.html', form=form)

@app.route('/files/<int:fileid>/codes')
@login_required
def manage_codes_for_file(fileid):
     userid = session['userid']
     file = File.query.get(fileid)
     return render_template('codes_file.html',codes=file.codes,file=file)

@app.route('/files/<int:fileid>/codes/add')
@login_required
def add_code_for_file(fileid):
     userid = session['userid']
     file = File.query.get(fileid)
     code = Code()
     code.fileid = file.id
     code.userid = userid
     db.session.add(code)
     db.session.commit()
     flash('code created')
     return redirect(url_for('manage_codes_for_file',fileid=file.id))

@app.route('/codes/<int:codeid>/delete')
@login_required
def delete_code(codeid):
     userid = session['userid']
     code = Code.query.get(codeid)
     db.session.delete(code)
     db.session.commit()
     flash('code deleted')
     return redirect(request.referrer)

@app.route('/codes/downloadform', methods=['get', 'post'])
def downloadform():
    form = DownloadForm()
    if form.validate_on_submit():
        downloadcode = form.code.data
        return redirect(url_for('view_code',codeid=downloadcode.strip()))
    return render_template('downloadform.html',form=form)

@app.route('/codes/<codeid>')
def view_code(codeid):
     code = Code.query.filter_by(code=codeid).first()
     if code is None:
         flash('download code not found','error')
         return redirect(url_for('index'))
     ip = request.remote_addr
     if code.downloaded and not code.ip == ip:
         flash('code has allready been used by another ip address','error')
         return redirect(url_for('index'))
     return render_template('code.html',code=code)

@app.route('/codes/<codeid>/download')
def download_code(codeid):
     print codeid
     code = Code.query.filter_by(code=codeid).first()
     if code is None:
         flash('download code not found','error')
         return redirect(url_for('index'))
     ip = request.remote_addr
     if code.downloaded and not code.ip == ip:
         flash('code has allready been used by another ip address','error')
         return redirect(url_for('index'))
     code.downloaded = True
     code.downloaded_at = datetime.now()
     code.ip = ip
     db.session.add(code)
     db.session.commit()
     return send_file(io.BytesIO(code.file.data),as_attachment=True,attachment_filename=code.file.filename)
     
