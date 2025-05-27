
def get_leaderboard_data(sheet):
    records = sheet.get_all_records()
    students = {}
    for record in records:
        student_id = record.get("student_id")
        hours = float(record.get("hours", 0))
        if student_id in students:
            students[student_id]["hours"] += hours
        else:
            students[student_id] = {
                "name": record.get("student_name", "Unknown"),
                "hours": hours
            }
    sorted_students = sorted(
        students.values(),
        key=lambda x: (-x["hours"], x["name"])
    )
    return sorted_students
