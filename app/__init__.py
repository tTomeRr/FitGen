from flask import Flask
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.secret_key = os.getenv('APP_SECRET_KEY')

    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_uri = f"postgresql://{db_user}:{db_password}@localhost/flex"
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    db.init_app(app)

    with app.app_context():
        from .routes import main as main_blueprint
        app.register_blueprint(main_blueprint)

    return app
