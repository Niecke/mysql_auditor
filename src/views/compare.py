# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request

from db import db
from model import Server


compare = Blueprint("compare", __name__, url_prefix="/compare")


@compare.route("/servers", methods=["GET", "POST"])
def servers():
    servers = Server.query.order_by(Server.host).all()
    server1_id = request.form.get("servers1", 0, type=int)
    server2_id = request.form.get("servers2", 0, type=int)
    user_compare = []

    if request.method == "POST":
        server1 = Server.query.get_or_404(server1_id)
        server2 = Server.query.get_or_404(server2_id)

        # compare the users
        users1 = server1.users
        users2 = server2.users

        users2_matched_ids = []

        # a user from users1 must be compared to each user from users2
        # since they are nerver perfect sorted
        for u1 in users1:
            found_u1_matching = False
            for u2 in users2:
                found_u1_matching, result = compare_users(u1, u2)
                if found_u1_matching:
                    user_compare.append({"user1": u1, "user2": u2, "diffs": result})
                    users2_matched_ids.append(u2.id)
                    break
            if not found_u1_matching:
                user_compare.append({"user1": u1, "user2": None, "diffs": []})

        for u2 in users2:
            if u2.id not in users2_matched_ids:
                user_compare.append({"user1": None, "user2": u2, "diffs": []})

    return render_template(
        "compare/servers.html",
        servers=servers,
        server1_id=server1_id,
        server2_id=server2_id,
        user_compare=user_compare,
    )


comparable_user_attributes = [
    "plugin",
    "authentication_string",
    "password_expired",
    "password_lifetime",
    "account_locked",
    "Create_role_priv",
    "Drop_role_priv",
    "Password_reuse_history",
    "Password_reuse_time",
    "Password_require_current",
    "User_attributes",
    "ssl_type",
    "ssl_cipher",
    "x509_issuer",
    "x509_subject",
    "Select_priv",
    "Insert_priv",
    "Update_priv",
    "Delete_priv",
    "Create_priv",
    "Drop_priv",
    "Reload_priv",
    "Shutdown_priv",
    "Process_priv",
    "File_priv",
    "Grant_priv",
    "References_priv",
    "Index_priv",
    "Alter_priv",
    "Show_db_priv",
    "Super_priv",
    "Create_tmp_table_priv",
    "Lock_tables_priv",
    "Execute_priv",
    "Repl_slave_priv",
    "Repl_client_priv",
    "Create_view_priv",
    "Show_view_priv",
    "Create_routine_priv",
    "Alter_routine_priv",
    "Create_user_priv",
    "Event_priv",
    "Trigger_priv",
    "Create_tablespace_priv",
    "max_questions",
    "max_updates",
    "max_connections",
    "max_user_connections",
]


def compare_users(u1, u2):
    # if username or host unequal the users are not the same
    if u1.User != u2.User or u1.Host != u2.Host:
        return False, []

    # if one of the following attributes differ then the users
    # are the same but with different config
    diffs = []
    for attr in comparable_user_attributes:
        if u1.__dict__.get(attr) != u2.__dict__.get(attr):
            # if comparing different mysql versions, it is possible that some values are NULL
            # because they don't exsist for one server
            v1 = u1.__dict__.get(attr) if u1.__dict__.get(attr) else "NULL"
            v2 = u2.__dict__.get(attr) if u2.__dict__.get(attr) else "NULL"
            diffs.append(
                (
                    attr,
                    v1,
                    v2,
                )
            )
    return True, diffs
