# -*- coding: utf-8 -*-
from flask import Blueprint, render_template


default = Blueprint("default", __name__, url_prefix="/")


@default.route("/")
def index():
    return render_template("default/index.html")


@default.route("/health")
def health():
    return {"status": "up"}
