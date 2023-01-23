# -*- coding: utf-8 -*-
from sqlalchemy.types import CHAR

from db import db


class DatabasePrivileges(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pull_counter = db.Column(db.BigInteger, default=0)
    server_id = db.Column(db.Integer, db.ForeignKey("server.id"), nullable=False)

    User = db.Column(db.String)
    Db = db.Column(db.String)
    Host = db.Column(db.String)

    Select_priv = db.Column(CHAR(1))
    Insert_priv = db.Column(CHAR(1))
    Update_priv = db.Column(CHAR(1))
    Delete_priv = db.Column(CHAR(1))
    Create_priv = db.Column(CHAR(1))
    Drop_priv = db.Column(CHAR(1))
    Grant_priv = db.Column(CHAR(1))
    References_priv = db.Column(CHAR(1))
    Index_priv = db.Column(CHAR(1))
    Alter_priv = db.Column(CHAR(1))
    Create_tmp_table_priv = db.Column(CHAR(1))
    Lock_tables_priv = db.Column(CHAR(1))
    Create_view_priv = db.Column(CHAR(1))
    Show_view_priv = db.Column(CHAR(1))
    Create_routine_priv = db.Column(CHAR(1))
    Alter_routine_priv = db.Column(CHAR(1))
    Execute_priv = db.Column(CHAR(1))
    Event_priv = db.Column(CHAR(1))
    Trigger_priv = db.Column(CHAR(1))
