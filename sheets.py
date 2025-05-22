
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1NEqywkP9k_Tp-GoNS400H3j7dRqb-tOOSPmhm-0dRbs")

def get_worksheet(tab_name):
    return sheet.worksheet(tab_name)

def add_student(surname, name, email, grade, school, password):
    students_ws = get_worksheet("students")
    admin_ws = get_worksheet("admin")

    existing_ids = students_ws.col_values(1)[1:]
    new_id = str(len(existing_ids) + 1).zfill(4)

    students_ws.append_row([new_id, surname, name, grade, school, 0])
    admin_ws.append_row([new_id, surname, name, email, grade, school, password, "", "", "", ""])
    return new_id

def email_exists(email):
    admin_ws = get_worksheet("admin")
    records = admin_ws.get_all_records()
    return any(row["email"] == email for row in records)

def check_login(email, password):
    admin_ws = get_worksheet("admin")
    records = admin_ws.get_all_records()
    for row in records:
        if row["email"] == email and row["password"] == password:
            return str(row["student_id"])
    return None

def log_hours(student_id, date, time, activity, hours, reflection=""):
    logs_ws = get_worksheet("logs")
    students_ws = get_worksheet("students")
    student_records = students_ws.get_all_records()

    # Find student’s name and surname
    for row in student_records:
        if str(row["student_id"]) == student_id:
            surname = row["surname"]
            name = row["name"]
            break
    else:
        surname = ""
        name = ""

    # Append to logs with correct structure
    logs_ws.append_row([
        student_id,      # A: student_id
        surname,         # B: surname
        name,            # C: name
        date,            # D: date
        time,            # E: time
        "",              # F: ip address (placeholder)
        "",              # G: location (placeholder)
        activity,        # H: activity
        hours,           # I: hours achieved
        reflection       # J: reflection
    ])

    # Update total hours in students sheet
    for i, row in enumerate(student_records):
        if str(row["student_id"]) == student_id:
            new_total = float(row["total_hours"]) + float(hours)
            students_ws.update_cell(i + 2, 6, new_total)  # Column 6 = total_hours
            break

    students_ws = get_worksheet("students")
    records = students_ws.get_all_records()
    for i, row in enumerate(records):
        if str(row["student_id"]) == student_id:
            new_total = float(row["total_hours"]) + float(hours)
            students_ws.update_cell(i + 2, 6, new_total)
            break

def get_student_logs(student_id):
    logs_ws = get_worksheet("logs")
    records = logs_ws.get_all_records()
    return [r for r in records if str(r["student_id"]) == student_id]

def get_total_hours(student_id):
    students_ws = get_worksheet("students")
    records = students_ws.get_all_records()
    for row in records:
        if str(row["student_id"]) == student_id:
            return float(row["total_hours"])
    return 0

def get_leaderboard():
    students_ws = get_worksheet("students")
    records = students_ws.get_all_records()
    return sorted(records, key=lambda x: float(x["total_hours"]), reverse=True)

def get_student_info(student_id):
    admin_ws = get_worksheet("admin")
    records = admin_ws.get_all_records()
    for row in records:
        if str(row["student_id"]) == student_id:
            return row
    return {}

def update_goal(student_id, goal):
    students_ws = get_worksheet("students")
    records = students_ws.get_all_records()
    for i, row in enumerate(records):
        if str(row["student_id"]) == student_id:
            students_ws.update_cell(i + 2, 7, goal)
            break

def get_goal(student_id):
    students_ws = get_worksheet("students")
    records = students_ws.get_all_records()
    for row in records:
        if str(row["student_id"]) == student_id:
            return float(row.get("goal", 0))
    return 0
