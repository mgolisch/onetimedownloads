import string
import random
from flask_script import Manager
from onetimedownloads import app, db
from onetimedownloads.models import User
manager = Manager(app)

@manager.option('-n', '--name', dest='name', default=None)
def adduser(name):
    """
    creates new users
    """
    if name is None:
        print 'no name specified .. aborting'
        return
    print 'adding user %s ' % name
    if User.query.filter_by(email=name).first() is not None:
        print 'user %s exists allready' % name
        return
    user = User()
    user.email = name
    user.password = ''.join(random.choice(string.ascii_uppercase +
                                          string.digits) for _ in range(8))
    db.session.add(user)
    db.session.commit()
    print 'user %s created' % name


@manager.option('-n', '--name', dest='name', default=None)
def deleteuser(name):
    """
    delete given user
    """
    if name is None:
        print 'no user specified'
        return

    print 'deleting user %s ' % name
    user = User.query.filter_by(email=name).first()
    if user is None:
        print 'user %s does not exist' % name
        return
    db.session.delete(user)
    db.session.commit()
    print 'user %s deleted' % name


@manager.command
def listuser():
    """
    lists all users in the User table
    """
    print 'listing users:'
    users = User.query.all()
    for user in users:
        print 'name: %s |password: %s' % (user.email, user.password)


@manager.command
def initdb():
    """
    recreate tables from models.py
    """
    db.drop_all()
    db.create_all()
    adduser('admin')

if __name__ == "__main__":
    manager.run()
