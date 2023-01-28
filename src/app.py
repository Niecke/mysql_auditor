# -*- coding: utf-8 -*-
from flask import Flask
from db import db

from views.default import default
from views.server import server
from views.config import config
from views.table_privs import table_privs
from views.db_privs import database_privs


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    db.init_app(app)

    try:
        with app.app_context():
            db.create_all()
    except:
        print("DB already setup")

    app.register_blueprint(default)
    app.register_blueprint(server)
    app.register_blueprint(config)
    app.register_blueprint(table_privs)
    app.register_blueprint(database_privs)

    return app
