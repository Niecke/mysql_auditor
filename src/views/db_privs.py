# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template

from model import Server, User, DatabasePrivileges


database_privs = Blueprint("database_privs", __name__, url_prefix="/database_privs")


@database_privs.route("/", methods=["GET", "POST"])
def list():
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
        DatabasePrivileges.query.with_entities(DatabasePrivileges.Db)
        .distinct(DatabasePrivileges.Db)
        .order_by(DatabasePrivileges.Db)
        .all()
    )
    server_id = None
    user = None
    database = None

    if request.method == "GET":
        database_privs_list = DatabasePrivileges.query.order_by(
            DatabasePrivileges.id
        ).all()

    elif request.method == "POST":
        server_id = request.form.get("servers", None)
        user = request.form.get("users", None)
        database = request.form.get("databases", None)
        queries = []
        if server_id:
            queries.append(DatabasePrivileges.server_id == server_id)
        if user:
            queries.append(DatabasePrivileges.User == user)
        if database:
            queries.append(DatabasePrivileges.Db == database)

        database_privs_list = (
            DatabasePrivileges.query.filter(*queries)
            .order_by(DatabasePrivileges.id)
            .all()
        )

    rendered_db_privs = []
    for database_priv in database_privs_list:
        l = map_db_grants(database_priv)
        s = f"GRANT {','.join(l)} ON {database_priv.Db}.* TO '{database_priv.User}'@'{database_priv.Host}'"
        rendered_db_privs.append({"s": s} | database_priv.__dict__)

    return render_template(
        "database_privs/list.html",
        database_privs=rendered_db_privs,
        servers=servers,
        server_id=server_id,
        users=users,
        username=user,
        databases=databases,
        database_name=database,
    )


def map_db_grants(priv):
    l = []
    if priv.Select_priv == "Y":
        l.append("SELECT")
    if priv.Insert_priv == "Y":
        l.append("INSERT")
    if priv.Update_priv == "Y":
        l.append("UPDATE")
    if priv.Delete_priv == "Y":
        l.append("DELETE")
    if priv.Create_priv == "Y":
        l.append("CREATE")
    if priv.Drop_priv == "Y":
        l.append("DROP")
    if priv.Grant_priv == "Y":
        l.append("GRANT")
    if priv.References_priv == "Y":
        l.append("REFERENCES")
    if priv.Index_priv == "Y":
        l.append("INDEX")
    if priv.Alter_priv == "Y":
        l.append("ALTER")
    if priv.Create_tmp_table_priv == "Y":
        l.append("CREATE TEMPORARY TABLES")
    if priv.Lock_tables_priv == "Y":
        l.append("LOCK TABLES")
    if priv.Create_view_priv == "Y":
        l.append("CREATE VIEW")
    if priv.Show_view_priv == "Y":
        l.append("SHOW VIEW")
    if priv.Create_routine_priv == "Y":
        l.append("CREATE ROUTINE")
    if priv.Alter_routine_priv == "Y":
        l.append("ALTER ROUTINE")
    if priv.Execute_priv == "Y":
        l.append("EXECUTE")
    if priv.Event_priv == "Y":
        l.append("EVENT")
    if priv.Trigger_priv == "Y":
        l.append("TRIGGER")
    return l
