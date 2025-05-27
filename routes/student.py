
from flask import Blueprint, render_template, request, session, redirect, flash

student_bp = Blueprint('student', __name__)

@student_bp.route("/start_log", methods=["POST"])
def start_log():
    # Dummy route placeholder
    return redirect("/log_hours")

@student_bp.route("/stop_log", methods=["POST"])
def stop_log():
    # Dummy route placeholder
    return redirect("/log_hours")

@student_bp.route("/my_hours")
def my_hours():
    # Dummy route placeholder
    return render_template("my_hours.html")

@student_bp.route("/profile")
def profile():
    # Dummy route placeholder
    return render_template("profile.html")

@student_bp.route("/update_goal", methods=["POST"])
def update_goal():
    # Dummy route placeholder
    return redirect("/profile")


from flask import current_app, jsonify

@student_bp.route("/session_debug")
def session_debug():
    if not current_app.debug:
        return "Session inspector only available in debug mode.", 403
    return jsonify(dict(session))
