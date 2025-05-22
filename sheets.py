
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
    student_id = str(student_id).zfill(4)

    logs_ws = get_worksheet("logs")
    students_ws = get_worksheet("students")

    students_data = students_ws.get_all_values()
    headers = students_data[0]
    student_rows = students_data[1:]  # skip header

    # Build a map of column names to index for safety
    header_index = {key.lower(): i for i, key in enumerate(headers)}

    # Find student by ID
    row_index = -1
    name = ""
    surname = ""
    for i, row in enumerate(student_rows):
        if row[header_index["student_id"]] == student_id:
            surname = row[header_index["surname"]]
            name = row[header_index["name"]]
            row_index = i + 2  # Adjust for 1-based index + header row
            break

    if row_index == -1:
        raise ValueError(f"Student ID {student_id} not found in 'students' sheet")

    # Append log (autofill name/surname in correct column order)
    logs_ws.append_row([
        student_id,  # A
        surname,     # B
        name,        # C
        date,        # D
        time,        # E
        "",          # F: ip
        "",          # G: location
        activity,    # H
        hours,       # I
        reflection   # J
    ])

    # Safely update total_hours in 'students'
    try:
        current_total = float(row[header_index["total hours"]])
    except (ValueError, IndexError):
        current_total = 0.0

    new_total = current_total + float(hours)
    students_ws.update_cell(row_index, header_index["total hours"] + 1, new_total)

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
