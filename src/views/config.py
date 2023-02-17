# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, current_app
import pymysql.cursors

from db import db
from model import Server, User, DatabasePrivileges, TablePrivileges


config = Blueprint("config", __name__, url_prefix="/config")


@config.route("/pull")
def pull_config():
    servers = Server.query.order_by(Server.id).all()

    pull_result = {"servers": 0, "failed": 0}

    for server in servers:
        pull_result["servers"] += 1
        try:
            connection = pymysql.connect(
                host=server.host,
                port=server.port,
                user=server.username,
                password=server.password,
                connect_timeout=3,
                cursorclass=pymysql.cursors.DictCursor,
            )

            with connection.cursor() as cursor:
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
                    ) or User(server_id=server.id)

                    user.pull_counter = new_pull_counter
                    for k in r:
                        setattr(user, k, r[k])
                    db.session.add(user)

                    db.session.commit()

                    update_database_privileges(
                        connection=connection,
                        server_id=server.id,
                        user=user,
                        new_pull_counter=new_pull_counter,
                    )

                    update_table_privileges(
                        connection=connection,
                        server_id=server.id,
                        user=user,
                        new_pull_counter=new_pull_counter,
                    )

                # at the end we check for users that have not been updated
                old_users = (
                    User.query.filter(User.server_id == server.id)
                    .filter(User.pull_counter == server.pull_counter)
                    .all()
                )
                for o in old_users:
                    db.session.delete(o)

                old_table_privs = (
                    TablePrivileges.query.filter(TablePrivileges.server_id == server.id)
                    .filter(TablePrivileges.pull_counter == server.pull_counter)
                    .all()
                )

                for o in old_table_privs:
                    db.session.delete(o)

                # at the end we check for users that have not been updated
                old_db_privs = (
                    DatabasePrivileges.query.filter(
                        DatabasePrivileges.server_id == server.id
                    )
                    .filter(DatabasePrivileges.pull_counter == server.pull_counter)
                    .all()
                )

                for o in old_db_privs:
                    db.session.delete(o)

                db.session.commit()

                server.pull_counter = new_pull_counter
                db.session.commit()
        except:
            # in case one server can not be reached; just skip it
            pull_result["failed"] += 1
            continue

    servers = Server.query.all()
    users = User.query.all()
    db_priv_cnt = DatabasePrivileges.query.count()
    table_priv_cnt = TablePrivileges.query.count()

    return render_template(
        "default/index.html",
        pull_result=pull_result,
        servers=servers,
        users=users,
        db_priv_cnt=db_priv_cnt,
        table_priv_cnt=table_priv_cnt,
    )


def update_database_privileges(connection, server_id, user, new_pull_counter):
    with connection.cursor() as cursor:
        stmt = f"SELECT * FROM mysql.db WHERE Host = '{user.Host}' AND User = '{user.User}'"
        cursor.execute(stmt)
        result = cursor.fetchall()

        for r in result:
            current_app.logger.debug(f"adding priv: {r}")
            db_priv = (
                DatabasePrivileges.query.filter(DatabasePrivileges.User == user.User)
                .filter(DatabasePrivileges.Host == user.Host)
                .filter(DatabasePrivileges.Db == r["Db"])
                .filter(DatabasePrivileges.server_id == server_id)
                .first()
            ) or DatabasePrivileges(server_id=server_id)

            db_priv.pull_counter = new_pull_counter
            for k in r:
                setattr(db_priv, k, r[k])
            db.session.add(db_priv)

            db.session.commit()


def update_table_privileges(connection, server_id, user, new_pull_counter):
    with connection.cursor() as cursor:
        stmt = f"SELECT * FROM mysql.tables_priv WHERE Host = '{user.Host}' AND User = '{user.User}'"
        current_app.logger.debug(stmt)
        cursor.execute(stmt)
        result = cursor.fetchall()
        current_app.logger.debug(f"fetched table_privs: {result}")

        for r in result:
            table_priv = (
                TablePrivileges.query.filter(TablePrivileges.User == user.User)
                .filter(TablePrivileges.Host == user.Host)
                .filter(TablePrivileges.Db == r["Db"])
                .filter(TablePrivileges.Table_name == r["Table_name"])
                .filter(TablePrivileges.server_id == server_id)
                .first()
            ) or TablePrivileges(server_id=server_id)

            table_priv.pull_counter = new_pull_counter
            for k in r:
                setattr(table_priv, k, r[k])
            current_app.logger.debug(f"adding table priv - {r['Table_name']}")
            db.session.add(table_priv)

            db.session.commit()


@config.route("/users")
def user_list():
    users = User.query.order_by(User.server_id).all()
    return render_template("default/users.html", users=users)


@config.route("/user/<int:user_id>")
def user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("default/user.html", user=user)
