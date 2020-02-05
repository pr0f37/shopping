from flask import Flask
from planner.models import db, login_manager
from planner.users.routes import bcrypt, users
from planner.users.utils import mail
from planner.recipes.routes import recipes
from planner.main.routes import main_bp
from planner.scraper.routes import scrap
from planner.shopping_list.routes import shopping
from planner.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    app.register_blueprint(users)
    app.register_blueprint(recipes)
    app.register_blueprint(main_bp)
    app.register_blueprint(scrap)
    app.register_blueprint(shopping)

    return app
