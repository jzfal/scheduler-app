# handle all CRUD operations


from app import db
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login



class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
    leaves = db.relationship('Leaves', backref = 'employee', lazy = 'dynamic')
    # back ref allows us to see the user given the leave, leave.author will return us the user id
    
    def __repr__(self):
        return '<User {}>'.format(self.username)    


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    # add in logic for admin later in roles




class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow) # pass the utc function, utc enables display of the local time
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Leaves(db.Model):
    __tablename__ = 'leaves'
    id = db.Column(db.Integer, primary_key = True)
    startdate = db.Column(db.Date)
    enddate = db.Column(db.Date)
    note = db.Column(db.String(140))
    halfdaybegin = db.Column(db.Boolean)
    halfdayend = db.Column(db.Boolean)
    employee_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # users = db.relationship('User')
    
    # setup the relationship

    def __repr__(self):
        return '<Leaves {}>'.format(self.note) # for debugging later







@login.user_loader
def load_user(id):
    """
    Flask login passes an id str to the db to get
    the user record from User table
    """
    return User.query.get(int(id))


