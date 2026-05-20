from flask import Flask
from flask_login import LoginManager
from app.models import db
from flask_migrate import Migrate
import os

migrate = Migrate()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///db.sqlite3")
    app.secret_key = os.environ.get("SECRET_KEY")

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Register Route
    from .auth.routes import auth
    app.register_blueprint(auth, url_prefix= "/auth")

    from .main.routes import main
    app.register_blueprint(main)

    from .quiz.routes import quiz_system    
    app.register_blueprint(quiz_system, url_prefix="/quiz")

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    return app
    