# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String, nullable=False)
    port = db.Column(db.Integer, default=3306)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
