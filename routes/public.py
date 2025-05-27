
from flask import Blueprint, render_template, request, redirect, session, flash

public_bp = Blueprint('public', __name__)

@public_bp.route("/")
def home():
    return render_template("home.html")

@public_bp.route("/login", methods=["GET", "POST"])
def login():
    # Dummy route placeholder
    return render_template("login.html")

@public_bp.route("/register", methods=["GET", "POST"])
def register():
    # Dummy route placeholder
    return render_template("register.html")

@public_bp.route("/logout")
def logout():
    # Dummy route placeholder
    return redirect("/")
