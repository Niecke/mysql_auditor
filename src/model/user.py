# -*- coding: utf-8 -*-
from sqlalchemy.types import CHAR

from db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pull_counter = db.Column(db.BigInteger, default=0)
    server_id = db.Column(db.Integer, db.ForeignKey("server.id"), nullable=False)

    User = db.Column(db.String, nullable=False)
    Host = db.Column(db.String, nullable=False)
    plugin = db.Column(db.String)
    authentication_string = db.Column(db.String)
    password_expired = db.Column(CHAR(1))
    password_last_changed = db.Column(db.String)
    password_lifetime = db.Column(db.String)
    account_locked = db.Column(CHAR(1))
    Create_role_priv = db.Column(CHAR(1))
    Drop_role_priv = db.Column(CHAR(1))
    Password_reuse_history = db.Column(db.String)
    Password_reuse_time = db.Column(db.String)
    Password_require_current = db.Column(db.String)
    User_attributes = db.Column(db.String)

    # SSL
    ssl_type = db.Column(db.String)
    ssl_cipher = db.Column(db.String)
    x509_issuer = db.Column(db.String)
    x509_subject = db.Column(db.String)

    # Global Privs
    Select_priv = db.Column(CHAR(1))
    Insert_priv = db.Column(CHAR(1))
    Update_priv = db.Column(CHAR(1))
    Delete_priv = db.Column(CHAR(1))
    Create_priv = db.Column(CHAR(1))
    Drop_priv = db.Column(CHAR(1))
    Reload_priv = db.Column(CHAR(1))
    Shutdown_priv = db.Column(CHAR(1))
    Process_priv = db.Column(CHAR(1))
    File_priv = db.Column(CHAR(1))
    Grant_priv = db.Column(CHAR(1))
    References_priv = db.Column(CHAR(1))
    Index_priv = db.Column(CHAR(1))
    Alter_priv = db.Column(CHAR(1))
    Show_db_priv = db.Column(CHAR(1))
    Super_priv = db.Column(CHAR(1))
    Create_tmp_table_priv = db.Column(CHAR(1))
    Lock_tables_priv = db.Column(CHAR(1))
    Execute_priv = db.Column(CHAR(1))
    Repl_slave_priv = db.Column(CHAR(1))
    Repl_client_priv = db.Column(CHAR(1))
    Create_view_priv = db.Column(CHAR(1))
    Show_view_priv = db.Column(CHAR(1))
    Create_routine_priv = db.Column(CHAR(1))
    Alter_routine_priv = db.Column(CHAR(1))
    Create_user_priv = db.Column(CHAR(1))
    Event_priv = db.Column(CHAR(1))
    Trigger_priv = db.Column(CHAR(1))
    Create_tablespace_priv = db.Column(CHAR(1))

    # Limits
    max_questions = db.Column(db.Integer)
    max_updates = db.Column(db.Integer)
    max_connections = db.Column(db.Integer)
    max_user_connections = db.Column(db.Integer)
