import flask
import toml
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


def create_app(config=None) -> flask.Flask:
    app = flask.Flask(__name__, instance_relative_config=True)

    if config is None:
        app.config.from_file('configdev.toml', load=toml.load, silent=True)
        print("config is configdev.toml")
    else:
        app.config.from_file(config, load=toml.load, silent=True)
        print(f"config is {config}")


    with app.app_context():
        create_services(app)
    return app


def create_services(app):
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)

    db.create_all()
    db.session.commit()

    from . import auth
    app.register_blueprint(auth.auth)

    from . import blog
    app.register_blueprint(blog.blog)

    from .api import set_resources
    set_resources()