from flask import render_template, redirect, url_for, flash, abort, request
from adapp import app, db, bcrypt
from adapp.models import User, Ad
from adapp.forms import RegistrationForm, LoginForm, CreatingAdForm, EditProfileForm, PickUserForm, FinishAdForm
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
        flash('You are already logged in')
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Wrong email or password!')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('Successfully logged out!')
    return redirect(url_for('home'))

@app.route('/create_ad', methods=['POST', 'GET'])
@login_required
def create_ad():
    form = CreatingAdForm()
    if form.validate_on_submit():
        new_ad = Ad(title=form.title.data, content=form.content.data, date_of_create=datetime.now(), reward=form.reward.data)
        new_ad.user_id = current_user.id
        db.session.add(new_ad)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_ad.html', form=form, legend='Create ad!')

@app.route('/ad_detail/<int:ad_id>')
def ad_detail(ad_id):
    ad = Ad.query.get_or_404(ad_id)
    form = PickUserForm()
    finish_form = FinishAdForm()
    return render_template('ad_detail.html', ad=ad, form=form, finish_form=finish_form)

@app.route('/ad_update/<int:ad_id>', methods=['GET', 'POST'])
@login_required
def update_ad(ad_id):
    ad = Ad.query.get_or_404(ad_id)
    if ad.author != current_user:
        abort(404)
    form = CreatingAdForm()
    if request.method == 'GET':
        form.title.data = ad.title
        form.content.data = ad.content
        form.reward.data = ad.reward
    elif form.validate_on_submit():
        ad.title = form.title.data
        ad.content = form.content.data
        ad.reward = form.reward.data
        db.session.commit()
        flash('Successfully updated!')
        return redirect(url_for('ad_detail', ad_id=ad.id))
    return render_template('create_ad.html', ad=ad, legend='Update ad!', form=form)

@app.route('/delete_ad/<int:ad_id>')
@login_required
def delete_ad(ad_id):
    ad = Ad.query.get_or_404(ad_id)
    if ad.author != current_user:
        abort(404)
    db.session.delete(ad)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/sign_in/<int:ad_id>')
@login_required
def sign_in(ad_id):
    ad = Ad.query.get_or_404(ad_id)
    if ad.is_finished:
        flash('This ad is already finished, you cannot sign in!')
    ad.users.append(current_user)
    db.session.commit()
    return redirect(url_for('ad_detail', ad_id=ad.id))

@app.route('/user_detail/<int:user_id>')
@login_required
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_detail.html', user=user)

@app.route('/update_profile/<int:user_id>', methods=['GET', 'POST'])
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

@app.route('/pick_user/<int:ad_id>/<int:user_id>', methods=['POST'])
@login_required
def pick_user(ad_id, user_id):
    ad = Ad.query.get_or_404(ad_id)
    user = User.query.get_or_404(user_id)
    form = PickUserForm()
    finish_form = FinishAdForm()
    if form.validate_on_submit():
        user.picked_for_ads.append(ad)
        db.session.commit()
    return render_template('ad_detail.html', ad=ad, form=form, user=user, finish_form=finish_form)

@app.route('/finish_ad/<int:ad_id>', methods=['GET', 'POST'])
@login_required
def finish_ad(ad_id):
    ad = Ad.query.get_or_404(ad_id)
    if ad.author != current_user or ad.picked_for is None:
        abort(404)
    finish_form = FinishAdForm()
    if finish_form.validate_on_submit():
        ad.is_finished = True
        db.session.commit()
    return render_template('ad_detail.html', ad=ad, finish_form=finish_form)