
# HourTracker Web App

A fully functional Flask + Google Sheets-based Progressive Web App (PWA) for logging, tracking, and managing student community service hours.

## Features

### Core Functionality
- **Student Registration** with school, grade, email, and password
- **Smart Hour Logging**
  - Start/Stop button-based logger
  - Captures activity, IP, location, device info
  - Auto-verifies based on expected duration and metadata
- **Log Verification System**
  - Marks logs as `verified`, `unverified`, or `suspicious`
  - Flags mismatches in device or location
- **Goal Tracking**
  - Set personal hour goal
  - Track total hours logged
  - Visual progress bar on profile
- **Log Filters**
  - Search by activity, date, status
- **Visual Analytics**
  - Pie chart summary of hours by activity using Chart.js

### Admin Panel
- Hardcoded login (`admin` / `admin123`)
- Access to sensitive logs and dashboard

### Advanced GUI (2025 Upgrade)
- Responsive mobile-first layout
- Soft geometric background + dark container overlay
- Modern fonts and smooth button styling

### PWA Support
- Includes manifest.json and service worker (optional offline caching)
- Installable from browser on mobile

---

## Setup Instructions (Render Compatible)

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Google Sheets Setup**
- Use `credentials.json` from Google Cloud console
- Share your spreadsheet with the service account email
- Create tabs: `students`, `logs`, `admin`

3. **Run the App Locally**
```bash
python app.py
```

4. **Deploy to Render**
- Connect GitHub repo with this code
- Set build command: `pip install -r requirements.txt`
- Set start command: `python app.py`
- Ensure `credentials.json` is included in `.renderignore` or added as secret

---

## Folder Structure
```
├── app.py               # Flask routes and views
├── sheets.py            # Google Sheets functions
├── static/
│   └── style.css        # Full responsive + visual theme
├── templates/           # HTML templates
│   └── *.html           # Pages for user flow
├── credentials.json     # Google Sheets service account (private)
├── requirements.txt     # Python dependencies
└── README.md
```

---

## Author & License
Developed for educational purposes — 2025 capstone. MIT License.
