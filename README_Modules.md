
# Refactor Phase 1: Route Modularization

This project has been modularized using Flask Blueprints to improve readability and maintainability.

## Folder Structure

```
HourTracker/
├── app.py               # Main Flask app that registers all routes
├── routes/
│   ├── public.py        # Public routes: /, /login, /register, /logout
│   ├── student.py       # Student routes: /start_log, /stop_log, /my_hours, /profile, /update_goal
│   └── admin.py         # Admin routes: /admin_login, /admin_dashboard, /admin_logout
├── templates/           # All HTML templates
├── static/              # CSS, JS, PWA files
├── sheets.py            # Google Sheets integration
├── requirements.txt     # Dependencies
├── README.md            # General project overview
└── README_Modules.md    # This file
```

## Route Summary

| Route              | File         | Description                    |
|-------------------|--------------|--------------------------------|
| `/`               | public.py    | Home                           |
| `/login`          | public.py    | Student login                  |
| `/register`       | public.py    | Student registration           |
| `/logout`         | public.py    | Logout                         |
| `/start_log`      | student.py   | Start smart logging session    |
| `/stop_log`       | student.py   | Stop logging, verify entry     |
| `/my_hours`       | student.py   | View own log history           |
| `/profile`        | student.py   | View profile + goal            |
| `/update_goal`    | student.py   | Update goal                    |
| `/admin_login`    | admin.py     | Admin login                    |
| `/admin_dashboard`| admin.py     | Admin dashboard                |
| `/admin_logout`   | admin.py     | Admin logout                   |

## Benefits of Modularization

- Easier to debug and test separate parts of the app
- Improved structure for future development or scaling
- Allows teams to work in parallel on separate files
