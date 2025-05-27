
from flask import Blueprint, render_template, request, redirect, session, flash

public_bp = Blueprint('public', __name__)

@public_bp.route("/")
def home():
    return render_template("home.html")

@public_bp.route("/login", methods=["GET", "POST"])
def login():
    # Dummy route placeholder
    return "Login route"

@public_bp.route("/register", methods=["GET", "POST"])
def register():
    # Dummy route placeholder
    return "Register route"

@public_bp.route("/logout")
def logout():
    # Dummy route placeholder
    return redirect("/")
