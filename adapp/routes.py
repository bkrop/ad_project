from flask import render_template, redirect, url_for, flash
from adapp import app, db, bcrypt
from adapp.models import User, Ad
from adapp.forms import RegistrationForm, LoginForm, CreatingAdForm
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime



@app.route('/home')
@app.route('/')
def home():
    ads = Ad.query.all()
    return render_template('home.html', ads=ads)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(email=form.email.data, password=hashed_password, name=form.name.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/create_ad', methods=['POST', 'GET'])
@login_required
def create_ad():
    form = CreatingAdForm()
    if form.validate_on_submit():
        new_ad = Ad(title=form.title.data, content=form.content.data, date_of_create=datetime.now())
        new_ad.user_id = current_user.id
        db.session.add(new_ad)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_ad.html', form=form)