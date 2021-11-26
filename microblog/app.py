"""
Flask app
"""
from flask import Flask
from config import Config
from microblog.extensions import db, migrate

def configure_extensions(app):
    # Flask-SQLAlchemy
    db.init_app(app)
    
    # Flask-Migrate
    migrate.init_app(app)

app = Flask('microblog')
app.config.from_object(Config)

configure_extensions(app)




from . import routes, models # noqa
