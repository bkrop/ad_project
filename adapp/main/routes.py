from flask import Blueprint, render_template
from adapp.models import Ad

main = Blueprint('main', __name__)

@main.route('/home')
@main.route('/')
def home():
    ads = Ad.query.all()
    return render_template('home.html', ads=ads)