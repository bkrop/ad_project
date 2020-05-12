from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_required, current_user
from datetime import datetime
from adapp.models import Ad, User, Message
from adapp.messagess.forms import CreateMessageForm
from adapp import db

messagess = Blueprint('messagess', __name__)

@messagess.route('/send_message/<int:user_id>', methods=['POST', 'GET'])
@login_required
def send_message(user_id):
    user = User.query.get_or_404(user_id)
    form = CreateMessageForm()
    if form.validate_on_submit():
        new_message = Message(content=form.content.data, by=current_user, to=user, date_of_create=datetime.now())
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for('users.user_detail', user_id=user.id))
    return render_template('send_message.html', form=form, user=user)

@messagess.route('/inbox')
@login_required
def inbox():
    messages = current_user.messages_received
    return render_template('inbox.html', messages=messages)