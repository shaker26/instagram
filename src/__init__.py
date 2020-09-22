import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


def initialise_logger(app):
    """
    Read environment config then initialise a 2MB rotating log
    """
    log_dir = app.config['LOG_DIR']
    log_level = app.config['LOG_LEVEL']

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    file_handler = RotatingFileHandler(log_dir + '/instagram.log', 'a', 2 * 1024 * 1024, 3)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))

    app.logger.addHandler(file_handler)
    app.logger.setLevel(log_level)


def init_flask_restful_routes(app):
    """
    Define the routes the API exposes using Flask-Restful.  See docs here
    http://flask-restful-cn.readthedocs.org/en/0.3.5/quickstart.html#endpoints
    """
    app.logger.info('Initialising API Routes')
    api = Api(app)

    from src.api.views.health_check import HealthCheck
    from src.api.views.users import Users

    api.add_resource(HealthCheck, '/api/v1/health-check', endpoint="health check")
    api.add_resource(Users, '/api/v1/instagram/user', endpoint="users endpoints")


""" 
Initialise the Flask app and config 
"""
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

env = os.getenv('MICRO_ENV', 'Dev')  # default to Dev if config environment var not set
app.config.from_object('src.config.{0}Config'.format(env))

db = SQLAlchemy(app)
migrate = Migrate()

migrate.init_app(app, db)

app.logger.debug('Initialising Blueprints')

initialise_logger(app)
app.logger.info('Instagram-api starting up :)')

init_flask_restful_routes(app)

# Import all models so that they are registered with SQLAlchemy
from src.models import users
from src.models import posts