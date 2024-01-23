from flask import Flask
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy

load_dotenv()  # This loads the variables from the .env file

# Instantiate SQLAlchemy outside of create_app
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Set configurations directly
    app.secret_key = "Sachin"
    db_uri = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@localhost:5433/flex"
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    # Initialize SQLAlchemy with the app instance
    db.init_app(app)

    with app.app_context():
        # Import parts of your application
        from .routes import main as main_blueprint
        app.register_blueprint(main_blueprint)

        # Here you can initialize other components of your app, like login managers, etc.

    return app
