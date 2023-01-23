# -*- coding: utf-8 -*-
from db import db


class TablePrivileges(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pull_counter = db.Column(db.BigInteger, default=0)
    server_id = db.Column(db.Integer, db.ForeignKey("server.id"), nullable=False)

    User = db.Column(db.String)
    Db = db.Column(db.String)
    Host = db.Column(db.String)

    Table_name = db.Column(db.String)
    Grantor = db.Column(db.String)
    Timestamp = db.Column(db.String)
    Table_priv = db.Column(db.String)
    Column_priv = db.Column(db.String)
