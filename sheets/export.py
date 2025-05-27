
import csv
from io import StringIO
from flask import Response

def export_logs_to_csv(sheet, log_type="all"):
    records = sheet.get_all_records()
    if log_type == "flagged":
        records = [r for r in records if r.get("status", "") == "suspicious"]

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=records[0].keys())
    writer.writeheader()
    writer.writerows(records)
    output.seek(0)

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename={log_type}_logs.csv"}
    )
