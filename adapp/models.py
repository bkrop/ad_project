from adapp import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

users = db.Table('ad_users',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('ad_id', db.Integer, db.ForeignKey('ad.id')))

class User(db.Model, UserMixin):
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(300), default='')
    ads = db.relationship('Ad', backref='author', lazy=True, foreign_keys='Ad.user_id')
    

    def __repr__(self):
        return f'{self.name}, {self.email}'

class Ad(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(300), nullable=False)
    reward = db.Column(db.String(100), nullable=False)
    date_of_create = db.Column(db.DateTime, nullable=False)
    users = db.relationship('User', secondary=users, backref=db.backref('users', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))