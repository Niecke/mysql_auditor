# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from model import Server, User, DatabasePrivileges, TablePrivileges

default = Blueprint("default", __name__, url_prefix="/")


@default.route("/")
def index():
    servers = Server.query.all()
    users = User.query.all()
    db_priv_cnt = DatabasePrivileges.query.count()
    table_priv_cnt = TablePrivileges.query.count()
    return render_template(
        "default/index.html",
        servers=servers,
        users=users,
        db_priv_cnt=db_priv_cnt,
        table_priv_cnt=table_priv_cnt,
    )


@default.route("/health")
def health():
    return {"status": "up"}
