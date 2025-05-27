
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1NEqywkP9k_Tp-GoNS400H3j7dRqb-tOOSPmhm-0dRbs")

def safe_get_worksheet(name):
    try:
        return safe_get_worksheet(name)
    except Exception:
        try:
            return sheet.add_worksheet(title=name, rows="100", cols="20")
        except Exception as e:
            print(f"[ERROR] Failed to create or access worksheet '{name}': {e}")
            return None

def safe_append_row(worksheet, row):
    if worksheet:
        try:
            worksheet.append_row(row)
        except Exception as e:
            print(f"[ERROR] Failed to append row: {e}")
    else:
        print("[ERROR] Worksheet is None — cannot append row.")
    try:
        worksheetsafe_append_row(row)
    except Exception as e:
        print(f"[ERROR] Failed to append row to worksheet: {e}")

def safe_get_records(worksheet):
    if worksheet:
        try:
            return worksheet.get_all_records()
        except Exception as e:
            print(f"[ERROR] Failed to fetch records: {e}")
            return []
    return []

# Startup tab verification
required_tabs = ["students", "logs", "admin"]
for tab_name in required_tabs:
    ws = safe_get_worksheet(tab_name)
    if ws:
        print(f"✔️ Sheet '{tab_name}' confirmed.")
    else:
        print(f"⚠️ Sheet '{tab_name}' could not be created or accessed.")


def get_all_records():
    try:
        pass  # TODO: Add logic to fetch records from sheet
    except Exception as e:
        print(f"[ERROR] Failed to get records: {e}")
        return []

def get_worksheet(tab_name):
    return safe_get_worksheet(tab_name)

def add_student(surname, name, email, grade, school, password, ip, location):
    students_ws = get_worksheet("students")
    admin_ws = get_worksheet("admin")

    existing_ids = students_ws.col_values(1)[1:]
    new_id = str(len(existing_ids) + 1).zfill(4)

    # Generate and use student_id safely
    student_records = students_wssafe_get_records()
    student_id = str(len(student_records) + 1).zfill(4)
    students_wssafe_append_row([student_id, surname, name, grade, school, 0])
    admin_wssafe_append_row([student_id, surname, name, email, grade, school, password, ip, location, ""])
    return new_id

def email_exists(email):
    admin_ws = get_worksheet("admin")
    records = admin_wssafe_get_records()
    return any(row["email"] == email for row in records)

def check_login(email, password):
    admin_ws = get_worksheet("admin")
    records = admin_wssafe_get_records()
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
    logs_wssafe_append_row([
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
    records = students_wssafe_get_records()
    for i, row in enumerate(records):
        if str(row["student_id"]) == student_id:
            new_total = float(row["total_hours"]) + float(hours)
            students_ws.update_cell(i + 2, 6, new_total)
            break

def get_student_logs(student_id):
    logs_ws = get_worksheet("logs")
    records = logs_wssafe_get_records()
    return [r for r in records if str(r["student_id"]) == student_id]

def get_total_hours(student_id):
    students_ws = get_worksheet("students")
    records = students_wssafe_get_records()
    for row in records:
        if str(row["student_id"]) == student_id:
            return float(row["total_hours"])
    return 0

def get_leaderboard():
    students_ws = get_worksheet("students")
    records = students_wssafe_get_records()
    return sorted(records, key=lambda x: float(x["total_hours"]), reverse=True)

def get_student_info(student_id):
    admin_ws = get_worksheet("admin")
    records = admin_wssafe_get_records()
    for row in records:
        if str(row["student_id"]) == student_id:
            return row
    return {}

def update_goal(student_id, goal):
    students_ws = get_worksheet("students")
    records = students_wssafe_get_records()
    for i, row in enumerate(records):
        if str(row["student_id"]) == student_id:
            students_ws.update_cell(i + 2, 7, goal)
            break

def get_goal(student_id):
    students_ws = get_worksheet("students")
    records = students_wssafe_get_records()
    for row in records:
        if str(row["student_id"]) == student_id:
            return float(row.get("goal", 0))
    return 0


def log_smart_activity(student_id, date, start, end, activity, hours, ip, location, device, verified, status_reason):
    new_row = [student_id, "", "", date, start, end, ip, location, activity, hours, device, verified, status_reason]
    logs_sheetsafe_append_row(new_row)
    logs_sheetsafe_append_row(new_row)


def get_registered_metadata(student_id):
    admin_sheet = safe_get_worksheet("admin")
    records = admin_sheetsafe_get_records()
    for record in records:
        if str(record.get("student_id")).strip() == str(student_id).strip():
            return {
                "device_info": record.get("device_info", ""),
                "location": record.get("location", "")
            }
    return {"device_info": "", "location": ""}

def is_log_suspicious(current_device, current_location, registered_metadata):
    status = "verified"
    reasons = []

    if registered_metadata["device_info"] and current_device.strip() != registered_metadata["device_info"].strip():
        status = "suspicious"
        reasons.append("Device mismatch")

    if registered_metadata["location"] and registered_metadata["location"].strip() != current_location.strip():
        status = "suspicious"
        reasons.append("Location mismatch")

    return status, "; ".join(reasons) if reasons else ""
