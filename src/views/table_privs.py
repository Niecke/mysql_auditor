# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template

from model import Server, User, TablePrivileges


table_privs = Blueprint("table_privs", __name__, url_prefix="/table_privs")


@table_privs.route("/", methods=["GET", "POST"])
def list():
    rendered_table_privs = []
    servers = (
        Server.query.with_entities(Server.id, Server.host).order_by(Server.host).all()
    )
    users = (
        User.query.with_entities(User.User)
        .distinct(User.User)
        .order_by(User.User)
        .all()
    )
    databases = (
        TablePrivileges.query.with_entities(TablePrivileges.Db)
        .distinct(TablePrivileges.Db)
        .order_by(TablePrivileges.Db)
        .all()
    )
    server_id = None
    user = None
    database = None

    if request.method == "GET":
        table_privs_list = TablePrivileges.query.order_by(TablePrivileges.id).all()

    elif request.method == "POST":
        server_id = request.form.get("servers", None)
        user = request.form.get("users", None)
        database = request.form.get("databases", None)
        queries = []
        if server_id:
            queries.append(TablePrivileges.server_id == server_id)
        if user:
            queries.append(TablePrivileges.User == user)
        if database:
            queries.append(TablePrivileges.Db == database)

        table_privs_list = (
            TablePrivileges.query.filter(*queries).order_by(TablePrivileges.id).all()
        )

    for table_priv in table_privs_list:
        privs_str = str(table_priv.Table_priv).upper()
        s = f"GRANT {privs_str} ON {table_priv.Db}.{table_priv.Table_name} TO '{table_priv.User}'@'{table_priv.Host}'"
        rendered_table_privs.append({"s": s} | table_priv.__dict__)
    return render_template(
        "table_privs/list.html",
        table_privs=rendered_table_privs,
        servers=servers,
        server_id=server_id,
        users=users,
        username=user,
        databases=databases,
        database_name=database,
    )
