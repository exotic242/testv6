
from flask import Flask, render_template, request, redirect, session, flash, Response
from sheets import (
    add_student, check_login, email_exists, log_hours, get_student_logs, get_total_hours,
    get_leaderboard, get_student_info, update_goal, get_goal
)
from datetime import datetime
import os
import csv

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        surname = request.form["surname"]
        name = request.form["name"]
        email = request.form["email"]
        grade = request.form["grade"]
        school = request.form["school"]
        password = request.form["password"]

        if email_exists(email):
            flash("Email already registered. Please log in.", "error")
            return redirect("/login")

        student_id = add_student(surname, name, email, grade, school, password)
        session["student_id"] = student_id
        flash(f"Registration successful. Your Student ID is {student_id}", "success")
        return redirect("/")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        student_id = check_login(email, password)
        if student_id:
            session["student_id"] = student_id
            flash("Login successful.", "success")
            return redirect("/")
        else:
            flash("Invalid email or password.", "error")
            return redirect("/login")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect("/")

@app.route("/log", methods=["GET", "POST"])
def log_hours_route():
    if "student_id" not in session:
        flash("Please log in to submit hours.", "error")
        return redirect("/login")

    if request.method == "POST":
        date = request.form["date"]
        time_ = request.form["time"]
        activity = request.form["activity_other"] if request.form["activity_select"] == "Other" else request.form["activity_select"]
        hours = request.form["hours"]
        reflection = request.form.get("reflection", "")

        log_hours(session["student_id"], date, time_, activity, hours, reflection)
        flash("Hours submitted successfully.", "success")
        return redirect("/my-hours")

    return render_template("log_hours.html")

@app.route("/my-hours")
def my_hours():
    if "student_id" not in session:
        flash("Please log in to view your hours.", "error")
        return redirect("/login")

    logs = get_student_logs(session["student_id"])
    total = get_total_hours(session["student_id"])
    goal = get_goal(session["student_id"])
    return render_template("my_hours.html", logs=logs, total=total, goal=goal)

@app.route("/leaderboard")
def leaderboard():
    records = get_leaderboard()
    return render_template("leaderboard.html", records=records)

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form["password"]
        if password == "admin123":
            session["is_admin"] = True
            flash("Admin mode activated.", "success")
            return redirect("/admin-dashboard")
        else:
            flash("Incorrect password.", "error")
            return redirect("/admin-login")
    return render_template("admin_login.html")

@app.route("/admin-dashboard")
def admin_dashboard():
    if not session.get("is_admin"):
        return "403 Forbidden", 403
    return render_template("admin_dashboard.html")

@app.route("/export-hours")
def export_hours():
    if "student_id" not in session:
        flash("Please log in to export your hours.", "error")
        return redirect("/login")

    logs = get_student_logs(session["student_id"])
    si = [["Date", "Time", "Activity", "Hours", "Reflection"]]
    for row in logs:
        si.append([row["date"], row["time"], row["activity"], row["hours"], row["reflection"]])

    csv_data = "\n".join([",".join(map(str, r)) for r in si])
    response = Response(csv_data, mimetype="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename=myhours{session['student_id']}.csv"
    return response

@app.route("/set-goal", methods=["POST"])
def set_goal():
    if "student_id" not in session:
        flash("Please log in.", "error")
        return redirect("/login")

    goal = request.form["goal"]
    update_goal(session["student_id"], goal)
    flash("Goal updated successfully.", "success")
    return redirect("/my-hours")

@app.route("/profile")
def profile():
    if "student_id" not in session:
        flash("Please log in to view your profile.", "error")
        return redirect("/login")

    student_id = session["student_id"]
    info = get_student_info(student_id)
    total = get_total_hours(student_id)
    goal = get_goal(student_id)

    return render_template("profile.html", info=info, total=total, goal=goal)

@app.route("/certificate")
def certificate():
    if "student_id" not in session:
        flash("Please log in.", "error")
        return redirect("/login")

    info = get_student_info(session["student_id"])
    total = get_total_hours(session["student_id"])
    current_date = datetime.now().strftime("%Y-%m-%d")

    return render_template("certificate.html", info=info, total=total, current_date=current_date)

if __name__ == "__main__":
    app.run(debug=True)
