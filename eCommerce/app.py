from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = "S`.H73y@AcMt(M'jXwp'(I;ngf^Sc5"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

    db.init_app(app)

    #User Sessions
    from models import User

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Importing blueprints
    from login.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from login.profile import user_profile as profile_blueprint
    app.register_blueprint(profile_blueprint)

    return app