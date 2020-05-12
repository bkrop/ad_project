from flask import Blueprint, render_template, url_for, redirect, abort, request, flash
from flask_login import login_required, current_user
from datetime import datetime
from adapp.ads.forms import CreatingAdForm, PickUserForm, FinishAdForm
from adapp import db
from adapp.models import Ad, User

ads = Blueprint('ads', __name__)

@ads.route('/create_ad', methods=['POST', 'GET'])
@login_required
def create_ad():
    form = CreatingAdForm()
    if form.validate_on_submit():
        new_ad = Ad(title=form.title.data, content=form.content.data, date_of_create=datetime.now(), reward=form.reward.data)
        new_ad.user_id = current_user.id
        db.session.add(new_ad)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('create_ad.html', form=form, legend='Create ad!')

@ads.route('/ad_detail/<int:ad_id>')
def ad_detail(ad_id):
    ad = Ad.query.get_or_404(ad_id)
    form = PickUserForm()
    finish_form = FinishAdForm()
    return render_template('ad_detail.html', ad=ad, form=form, finish_form=finish_form)

@ads.route('/ad_update/<int:ad_id>', methods=['GET', 'POST'])
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
        flash('Successfully updated!', 'success')
        return redirect(url_for('ad_detail', ad_id=ad.id))
    return render_template('create_ad.html', ad=ad, legend='Update ad!', form=form)

@ads.route('/delete_ad/<int:ad_id>')
@login_required
def delete_ad(ad_id):
    ad = Ad.query.get_or_404(ad_id)
    if ad.author != current_user:
        abort(404)
    db.session.delete(ad)
    db.session.commit()
    return redirect(url_for('main.home'))

@ads.route('/sign_in/<int:ad_id>')
@login_required
def sign_in(ad_id):
    ad = Ad.query.get_or_404(ad_id)
    if ad.is_finished:
        flash('This ad is already finished, you cannot sign in!')
    ad.users.append(current_user)
    db.session.commit()
    return redirect(url_for('ads.ad_detail', ad_id=ad.id))

@ads.route('/pick_user/<int:ad_id><int:user_id>', methods=['POST'])
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

@ads.route('/finish_ad/<int:ad_id>', methods=['GET', 'POST'])
@login_required
def finish_ad(ad_id):
    ad = Ad.query.get_or_404(ad_id)
    if ad.author != current_user or ad.picked_for is None:
        abort(404)
    finish_form = FinishAdForm()
    if finish_form.validate_on_submit():
        ad.is_finished = True
        db.session.commit()
        return redirect(url_for('rates.rate_user', user_id=ad.picked_for.id, ad_id=ad.id))
    return render_template('ad_detail.html', ad=ad, finish_form=finish_form)