# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from model import Server, User, DatabasePrivileges, TablePrivileges

default = Blueprint("default", __name__, url_prefix="/")


@default.route("/")
def index():
    server_cnt = Server.query.count()
    user_cnt = User.query.count()
    db_priv_cnt = DatabasePrivileges.query.count()
    table_priv_cnt = TablePrivileges.query.count()
    return render_template(
        "default/index.html",
        server_cnt=server_cnt,
        user_cnt=user_cnt,
        db_priv_cnt=db_priv_cnt,
        table_priv_cnt=table_priv_cnt,
    )


@default.route("/health")
def health():
    return {"status": "up"}
