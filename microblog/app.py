"""
Flask app
"""
import logging
import sys
from flask import Flask
from config import Config
from microblog.extensions import db, migrate
from microblog import routes

def create_app(config=Config, instance_path=None):
    """Creates the app.
    
    :param instance_path: An alternative instance path for the application.
                          By default the folder ``'instance'`` next to the
                          package or module is assumed to be the instance
                          path.
                          See :ref:`Instance Folders <flask:instance-folders>`.
    :param config: The configuration file or object.
                   The environment variable is weightet as the heaviest.
                   For example, if the config is specified via an file
                   and a ENVVAR, it will load the config via the file and
                   later overwrite it from the ENVVAR.
                   If no config is provided, FlaskBB will try to load the
                   config named ``flaskbb.cfg`` from the instance path.
    """
    app = Flask('microblog')
    configure_app(app, config)
    configure_extensions(app)
    configure_blueprints(app)
    
    return app


def configure_app(app, config):
    """ Configures microblog """
    app.config.from_object(config)

def configure_extensions(app):
    # Flask-SQLAlchemy
    db.init_app(app)
    
    # Flask-Migrate
    migrate.init_app(app, db)
    
def configure_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(routes.bp)
    return None


def configure_logger(app):
    """ Configure loggers """
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
        
def configure_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"db": db }

    app.shell_context_processor(shell_context)
    
# from . import models # noqa
    