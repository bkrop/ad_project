from adapp import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    ads = db.relationship('Ad', backref='author', lazy=True)

    def __repr__(self):
        return f'User: {self.email}, {self.name}'

class Ad(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(300), nullable=False)
    date_of_create = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))