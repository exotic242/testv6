

# Moved from sheets.py
def safe_get_worksheet(name):
    try:
        return safe_get_worksheet(name)
    except Exception:
        try:
            return sheet.add_worksheet(title=name, rows="100", cols="20")
        except Exception as e:
            print(f"[ERROR] Failed to create or access worksheet '{name}': {e}")
            return None

def safe_get_records(worksheet):
    if worksheet:
        try:
            return worksheet.get_all_records()
        except Exception as e:
            print(f"[ERROR] Failed to fetch records: {e}")
            return []
    return []

