# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request

from model import Server
from static import comparable_user_attributes, comparable_db_attributes


compare = Blueprint("compare", __name__, url_prefix="/compare")


@compare.route("/servers", methods=["GET", "POST"])
def servers():
    servers = Server.query.order_by(Server.host).all()
    server1_id = request.form.get("servers1", 0, type=int)
    server2_id = request.form.get("servers2", 0, type=int)
    user_compare = []
    database_compare = []

    if request.method == "POST":
        server1 = Server.query.get_or_404(server1_id)
        server2 = Server.query.get_or_404(server2_id)

        user_compare = compare_users(server1.users, server2.users)

        database_compare = compare_databases(
            server1.database_privileges, server2.database_privileges
        )

    return render_template(
        "compare/servers.html",
        servers=servers,
        server1_id=server1_id,
        server2_id=server2_id,
        user_compare=user_compare,
        database_compare=database_compare,
    )


def compare_users(users1, users2):
    user_compare = []
    users2_matched_ids = []

    # a user from users1 must be compared to each user from users2
    # since they are nerver perfect sorted
    for u1 in users1:
        found_u1_matching = False
        for u2 in users2:
            found_u1_matching, result = compare_attributes(
                u1,
                u2,
                comparable_user_attributes.get("first_compare"),
                comparable_user_attributes.get("second_compare"),
            )
            if found_u1_matching:
                user_compare.append({"user1": u1, "user2": u2, "diffs": result})
                users2_matched_ids.append(u2.id)
                break
        if not found_u1_matching:
            user_compare.append({"user1": u1, "user2": None, "diffs": []})

    for u2 in users2:
        if u2.id not in users2_matched_ids:
            user_compare.append({"user1": None, "user2": u2, "diffs": []})

    return user_compare


def compare_databases(databases1, databases2):
    database_compare = []
    databases2_matched_ids = []

    # a user from users1 must be compared to each user from users2
    # since they are nerver perfect sorted
    for d1 in databases1:
        found_d1_matching = False
        for d2 in databases2:
            found_d1_matching, result = compare_attributes(
                d1,
                d2,
                comparable_db_attributes.get("first_compare"),
                comparable_db_attributes.get("second_compare"),
            )
            if found_d1_matching:
                database_compare.append(
                    {"database1": d1, "database2": d2, "diffs": result}
                )
                databases2_matched_ids.append(d2.id)
                break
        if not found_d1_matching:
            database_compare.append({"database1": d1, "database2": None, "diffs": []})

    for d2 in databases2:
        if d2.id not in databases2_matched_ids:
            database_compare.append({"database1": None, "database2": d2, "diffs": []})

    return database_compare


def compare_attributes(c1, c2, first_compare, second_compare):
    for attr in first_compare:
        if c1.__dict__.get(attr) != c2.__dict__.get(attr):
            return False, []

    diffs = []
    for attr in second_compare:
        if c1.__dict__.get(attr) != c2.__dict__.get(attr):
            # if comparing different mysql versions, it is possible that some values are NULL
            # because they don't exsist for one server
            v1 = c1.__dict__.get(attr) if c1.__dict__.get(attr) else "NULL"
            v2 = c2.__dict__.get(attr) if c2.__dict__.get(attr) else "NULL"
            diffs.append(
                (
                    attr,
                    v1,
                    v2,
                )
            )
    return True, diffs
