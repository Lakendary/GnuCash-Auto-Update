from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from configparser import ConfigParser
from routes import main as main_blueprint

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
    app.config['SQLALCHEMY_DATABASE_URI'] = config['database']['uri']
    app.config['SECRET_KEY'] = config['secret']['key']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(main_blueprint)

    return app

# Initialize the database separately
db = SQLAlchemy()

# Run the application
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
