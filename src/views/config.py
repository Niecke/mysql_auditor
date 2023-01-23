# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, current_app
import pymysql.cursors

from db import db
from model import Server, User, DatabasePrivileges


config = Blueprint("config", __name__, url_prefix="/config")


@config.route("/pull")
def pull_config():
    servers = Server.query.order_by(Server.id).all()

    for server in servers:
        connection = pymysql.connect(
            host=server.host,
            port=server.port,
            user=server.username,
            password=server.password,
            connect_timeout=3,
            cursorclass=pymysql.cursors.DictCursor,
        )

        with connection.cursor() as cursor, db.session.no_autoflush:
            stmt = "SELECT * FROM mysql.user"
            cursor.execute(stmt)
            result = cursor.fetchall()
            new_pull_counter = server.pull_counter + 1

            for r in result:
                user = (
                    User.query.filter(User.User == r["User"])
                    .filter(User.Host == r["Host"])
                    .filter(User.server_id == server.id)
                    .first()
                )

                # update the existing user
                if user:
                    user.pull_counter = new_pull_counter
                    for k in r:
                        setattr(user, k, r[k])
                # create a new user
                else:
                    user = User()
                    user.server_id = server.id
                    user.pull_counter = new_pull_counter
                    for k in r:
                        setattr(user, k, r[k])
                    db.session.add(user)

            # at the end we check for users that have not been updated
            old_users = (
                User.query.filter(User.server_id == server.id)
                .filter(User.pull_counter == server.pull_counter)
                .all()
            )
            for o in old_users:
                db.session.delete(o)

            update_database_privileges(
                connection=connection,
                server_id=server.id,
                user=user,
                new_pull_counter=new_pull_counter,
            )

            # update_table_privileges()

            server.pull_counter = new_pull_counter
            db.session.commit()

    users = User.query.order_by(User.id).all()
    return render_template("default/users.html", users=users)


def update_database_privileges(connection, server_id, user, new_pull_counter):
    with connection.cursor() as cursor:
        stmt = f"SELECT * FROM mysql.db WHERE Host = '{user.Host}' AND User = '{user.User}'"
        cursor.execute(stmt)
        result = cursor.fetchall()

        for r in result:
            current_app.logger.info(f"adding priv: {r}")
            db_priv = (
                DatabasePrivileges.query.filter(DatabasePrivileges.User == user.User)
                .filter(DatabasePrivileges.Host == user.Host)
                .filter(DatabasePrivileges.Db == r["Db"])
                .filter(DatabasePrivileges.server_id == server_id)
            ).first()

            if db_priv:
                current_app.logger.info(f"updating a priv [{db_priv}]")
                db_priv.pull_counter = new_pull_counter
                for k in r:
                    setattr(db_priv, k, r[k])
            else:
                current_app.logger.info("creating a new priv")
                db_priv = DatabasePrivileges()
                db_priv.server_id = server_id
                db_priv.pull_counter = new_pull_counter
                for k in r:
                    setattr(db_priv, k, r[k])
                db.session.add(db_priv)

            # at the end we check for users that have not been updated
            old_db_privs = (
                DatabasePrivileges.query.filter(DatabasePrivileges.User == user.User)
                .filter(DatabasePrivileges.Host == user.Host)
                .filter(DatabasePrivileges.Db == r["Db"])
                .filter(DatabasePrivileges.server_id == server_id)
                .filter(DatabasePrivileges.pull_counter == new_pull_counter - 1)
            )

            for o in old_db_privs:
                db.session.delete(o)


@config.route("/users")
def user_list():
    users = User.query.order_by(User.id).all()
    return render_template("default/users.html", users=users)


@config.route("/user/<int:user_id>")
def user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("default/user.html", user=user)


@config.route("/db_privs")
def db_priv_list():
    db_privs = DatabasePrivileges.query.order_by(DatabasePrivileges.id).all()
    current_app.logger.info(db_privs)
    rendered_db_privs = list()
    for db_priv in db_privs:
        current_app.logger.info(f"processing {db_priv}")
        l = map_grants(db_priv)
        s = f"GRANT {','.join(l)} ON {db_priv.Db}.* TO '{db_priv.User}'@'{db_priv.Host}'"
        rendered_db_privs.append({"s": s} | db_priv.__dict__)
    return render_template("default/db_privs.html", db_privs=rendered_db_privs)


def map_grants(priv):
    l = list()
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
