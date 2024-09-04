from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from configparser import ConfigParser
from routes import main as main_blueprint
from data import db  # Import db here after initializing it in data.py

# Initialize config file
def get_config():
    config = ConfigParser()
    config.read('config.ini')
    return config

# Create the Flask application and configure it
def create_app():
    config = get_config()

    # Initialize the Flask application
    app = Flask(__name__)

    # Configuration
    db_config = config['database']
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    app.config['SECRET_KEY'] = config['secret']['key']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(main_blueprint)

    return app

# Run the application
if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()  # Ensure that tables are created before the app runs
    app.run(debug=True)