# -*- coding: utf-8 -*-
import traceback

import pymysql.cursors
import sqlalchemy
from flask import Blueprint, current_app, redirect, render_template, request, url_for

from db import db
from model import Server, User, DatabasePrivileges, TablePrivileges

server = Blueprint("server", __name__, url_prefix="/server")


@server.route("/", methods=["GET"])
def list():
    servers = Server.query.order_by(Server.id).all()
    return render_template("server/list.html", servers=servers)


@server.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        server = Server()
        for k in request.form:
            setattr(server, k, request.form[k])

        try:
            db.session.add(server)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as ex:
            return render_template("server/create.html", request=request, error=ex)

        return redirect(url_for("server.list"))

    return render_template("server/create.html")


@server.route("/edit/<int:server_id>", methods=["GET", "POST"])
def edit(server_id):

    server = Server.query.get_or_404(server_id)

    if request.method == "POST":
        for k in request.form:
            setattr(server, k, request.form[k])

        try:
            db.session.add(server)
            db.session.commit()
            return redirect(url_for("server.list"))

        except sqlalchemy.exc.IntegrityError as ex:
            return render_template("server/edit.html", request=request, error=ex)

    return render_template("server/edit.html", server=server)


@server.route("/delete/<int:server_id>", methods=["GET", "POST"])
def delete(server_id):

    if request.method == "GET":
        return render_template("server/delete.html", server_id=server_id)

    elif request.method == "POST":
        with db.session.no_autoflush:
            server = Server.query.get_or_404(server_id)
            db.session.delete(server)
            users = User.query.filter(User.server_id == server_id).delete()
            db_privs = DatabasePrivileges.query.filter(
                DatabasePrivileges.server_id == server_id
            ).delete()
            table_privs = TablePrivileges.query.filter(
                TablePrivileges.server_id == server_id
            ).delete()
            current_app.logger.debug(
                f"Deleted server {server_id} with {users} user, {db_privs} database privileges and {table_privs} table privileges."
            )
            db.session.commit()

        return redirect(url_for("server.list"))


@server.route("/test/<int:server_id>", methods=["GET"])
def test(server_id):
    # Doing to sql queries might be not the best solution, but we avoid JS for now
    servers = Server.query.order_by(Server.id).all()

    server = Server.query.get_or_404(server_id)

    try:
        # Connect to the database
        connection = pymysql.connect(
            host=server.host,
            port=server.port,
            user=server.username,
            password=server.password,
            connect_timeout=3,
            cursorclass=pymysql.cursors.DictCursor,
        )

        with connection.cursor() as cursor:
            sql = "SELECT 1"
            cursor.execute(sql)
            cursor.fetchone()

        return render_template(
            "server/list.html",
            servers=servers,
            checked_server_id=server.id,
            check_result="ok",
        )

    except Exception:
        current_app.logger.info(traceback.print_exc())

        return render_template(
            "server/list.html",
            servers=servers,
            checked_server_id=server.id,
            check_result="fail",
        )
