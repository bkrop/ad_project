from flask import Blueprint, render_template, url_for, redirect, abort
from flask_login import login_required, current_user
from adapp.models import User, Ad, Rate, Comment
from adapp.rates.forms import RateUserForm
from datetime import datetime
from adapp import db

rates = Blueprint('rates', __name__)

@rates.route('/rate_user/<int:user_id><int:ad_id>', methods=['GET', 'POST'])
@login_required
def rate_user(user_id, ad_id):
    user = User.query.get_or_404(user_id)
    ad = Ad.query.get_or_404(ad_id)
    if ad.is_finished == False or ad.rates:
        abort(404)
    form = RateUserForm()
    if form.validate_on_submit():
        rate = form.rate.data
        if rate == 'thumb up':
            user.rating += 1
        else:
            user.rating -= 1
        new_rate = Rate()
        new_rate.ad_id = ad.id
        new_comment = Comment(content=form.comment.data, by=current_user, to=user, date_of_create=datetime.now())
        db.session.add(new_rate, new_comment)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('rate_user.html', user=user, form=form)