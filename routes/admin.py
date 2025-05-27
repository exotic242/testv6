
from flask import Blueprint, render_template, request, redirect, session, flash

admin_bp = Blueprint('admin', __name__)


from sheets import safe_get_worksheet, safe_get_records

@admin_bp.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        admin_sheet = safe_get_worksheet("admin")
        admins = safe_get_records(admin_sheet)
        admin_emails = [a["email"].strip().lower() for a in admins if "email" in a]

        if email.strip().lower() in admin_emails and password == "admin123":
            session["smart_log"] = session.get("smart_log", {})
            session["smart_log"]["email"] = email
            session["smart_log"]["is_admin"] = True
            return redirect("/admin_dashboard")
        else:
            flash("Invalid admin credentials", "danger")
    return render_template("admin_login.html")

@admin_bp.route("/admin_dashboard")
def admin_dashboard():
    if not session.get("smart_log", {}).get("is_admin"):
        return redirect("/admin_login")
    return render_template("admin_dashboard.html")

@admin_bp.route("/admin_logout")
def admin_logout():
    session.pop("smart_log", None)
    return redirect("/")

@admin_bp.route("/admin_dashboard")
def admin_dashboard():
    # Dummy route placeholder
    return render_template("admin_dashboard.html")

@admin_bp.route("/admin_logout")
def admin_logout():
    # Dummy route placeholder
    return redirect("/")
