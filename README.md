
# Student Hours Tracker (Community Service App)

This is a full-featured web application built with Flask and Google Sheets that allows high school students to track their community service hours, set personal goals, and download certificates of participation. It is designed to be installable as a Progressive Web App (PWA) and is fully deployable on Render with GitHub integration.

---

## Features

- **Student Registration & Login**
- **Google Sheets Backend** (no SQL required)
- **Log Hours** with date, time, activity, and reflection
- **Set & Track Hour Goals** with progress bar
- **Live Leaderboard** sorted by total hours
- **Downloadable CSV** of your personal logs
- **Generate Certificate** (PDF printable)
- **Admin Mode** (password-protected)
- **Search/Filter Logs**
- **Activity Type Dropdown + Reflection**
- **Activity Chart** (Pie graph via Chart.js)
- **Tooltips for All Buttons**

---

## Tech Stack

- Python 3 (Flask)
- Google Sheets API (`gspread`, `oauth2client`)
- HTML/CSS + Chart.js
- Gunicorn (for deployment)
- PWA-ready (manifest + service worker)

---

## File Structure

```
.
├── app.py                  # Flask routes and session logic
├── sheets.py               # Google Sheets data access
├── requirements.txt
├── static/
│   ├── style.css
│   ├── manifest.json
│   ├── service-worker.js
│   └── icons/
├── templates/
│   ├── base.html
│   ├── register.html
│   ├── login.html
│   ├── log_hours.html
│   ├── my_hours.html
│   ├── leaderboard.html
│   ├── profile.html
│   ├── certificate.html
│   └── admin_login.html / dashboard.html
```

---

## Setup Instructions (Local)

1. **Install Python + Pipenv or virtualenv (recommended)**
2. Clone or unzip the project folder
3. Place your Google Sheets `credentials.json` file in the root directory
4. Run:
   ```
   pip install -r requirements.txt
   python app.py
   ```
5. Navigate to `http://localhost:5000`

---

## Deployment Instructions (Render.com)

1. Push this project to GitHub
2. Go to [Render](https://render.com)
3. Click "New Web Service" → Connect to GitHub repo
4. Set:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Upload `credentials.json` manually in Render's secret file section

---

## Notes

- This app is fully offline-capable when installed as a PWA (except logging)
- All data is backed by Google Sheets — no database required
- Perfect for school PATs, portfolio projects, or community service platforms

---

## License

MIT License. Free to use and modify.

---

**Built with care by [Your Name]**
