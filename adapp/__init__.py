from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from adapp.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from adapp.ads.routes import ads
    from adapp.main.routes import main
    from adapp.messagess.routes import messagess
    from adapp.rates.routes import rates
    from adapp.users.routes import users
    app.register_blueprint(ads)
    app.register_blueprint(main)
    app.register_blueprint(messagess)
    app.register_blueprint(rates)
    app.register_blueprint(users)

    return app