from onetimedownloads import db
from uuid import uuid4


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    name = db.Column(db.String)
    password = db.Column(db.String)
    files = db.relationship('File', backref='user', lazy='dynamic')
    codes = db.relationship('Code', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User: %s' % self.email


class File(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    filename = db.Column(db.String)
    data = db.Column(db.LargeBinary)
    size = db.Column(db.Integer)
    created_at = db.Column(db.String)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    codes = db.relationship('Code', backref='file', lazy="dynamic")

    def __repr__(self):
        return '<File|user: %s | name: %s >' % (self.user, self.filename)


class Code(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    code = db.Column(db.String, unique=True)
    downloaded = db.Column(db.Boolean, default=False)
    ip = db.Column(db.String)
    downloaded_at = db.Column(db.String)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    fileid = db.Column(db.Integer, db.ForeignKey('file.id'))

    def __init__(self):
        self.code = str(uuid4())
    def __repr__(self):
        return '<Code|user: %s | name: %s >' % (self.user, self.file.filename)
