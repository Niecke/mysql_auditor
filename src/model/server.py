# -*- coding: utf-8 -*-
from db import db


class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String, nullable=False)
    port = db.Column(db.Integer, default=3306)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    pull_counter = db.Column(db.BigInteger, default=0)
    users = db.relationship("User", backref="server")
    database_privileges = db.relationship("DatabasePrivileges", backref="server")
    table_privileges = db.relationship("TablePrivileges", backref="server")
