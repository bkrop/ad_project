from flask import Blueprint, render_template, url_for, redirect, abort, request, flash
from flask_login import login_required, current_user, login_user, logout_user
from adapp.users.forms import RegistrationForm, EditProfileForm, LoginForm
from adapp.models import User
from adapp import db, bcrypt

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(email=form.email.data, password=hashed_password, name=form.name.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('register.html', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in')
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.home'))
        else:
            flash('Wrong email or password!')
    return render_template('login.html', form=form)

@users.route('/logout')
def logout():
    logout_user()
    flash('Successfully logged out!', 'success')
    return redirect(url_for('main.home'))

@users.route('/user_detail/<int:user_id>')
@login_required
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    if current_user == user:
        return redirect(url_for('users.update_profile', user_id=current_user.id))
    return render_template('user_detail.html', user=user)

@users.route('/update_profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def update_profile(user_id):
    user = User.query.get_or_404(user_id)
    if current_user != user:
        abort(404)
    form = EditProfileForm()
    if form.validate_on_submit():
        user.description = form.description.data
        db.session.commit()
        flash('Profile updated!')
    elif request.method == 'GET':
        form.description.data = user.description
    return render_template('update_profile.html', form=form)