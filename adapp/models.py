from adapp import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

users = db.Table('ad_users',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('ad_id', db.Integer, db.ForeignKey('ad.id')))

users_picked_for = db.Table('users_picked_for',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('ad_id', db.Integer, db.ForeignKey('ad.id')))

class User(db.Model, UserMixin):
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(300), default='')
    rating = db.Column(db.Integer, default=0)
    ads = db.relationship('Ad', backref='author', lazy=True, foreign_keys='Ad.user_id')
    picked_for_ads = db.relationship('Ad', secondary=users_picked_for, backref=db.backref('picked_for', lazy=True, uselist=False))
    comments_sent = db.relationship('Comment', backref='by', lazy=True, foreign_keys='Comment.user_id')
    comments_received = db.relationship('Comment', backref='to', lazy=True, foreign_keys='Comment.recipient_id')
    

    def __repr__(self):
        return f'{self.name}, {self.email}'

class Ad(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(300), nullable=False)
    reward = db.Column(db.String(100), nullable=False)
    date_of_create = db.Column(db.DateTime, nullable=False)
    is_finished = db.Column(db.Boolean, default=False)
    rates = db.relationship('Rate', backref='concerns', lazy=True, foreign_keys='Rate.ad_id')
    users = db.relationship('User', secondary=users, backref=db.backref('users', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Rate(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    ad_id = db.Column(db.Integer, db.ForeignKey('ad.id'))

class Comment(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    content = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
