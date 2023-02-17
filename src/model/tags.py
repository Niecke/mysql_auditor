# -*- coding: utf-8 -*-
from db import db


class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
