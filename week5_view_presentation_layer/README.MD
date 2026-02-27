# Merrimack River Cruises – Web Application (Flask GUI)

**Course:** CSC6302 Database Principles  
**Module:** 05 GUI View Layer  
**Author:** Shaun Clarke

---

## Project Overview

This module replaces the CLI view from Module 04 with a full **Flask web application**. The three-tier architecture (View → BLL → DAL) is preserved, with `app.py` now serving as the web-based view layer. Users log in via a browser, then interact with the MRC database through a clean web UI adding passengers, vessels, and trips, and viewing all trip history in a formatted table.

Database credentials are loaded from a `config.ini` file rather than runtime prompts, making the app suitable for persistent web deployment.

---

## Architecture

```
Browser  →  app.py (Flask View)  →  bll.py (Business Logic)  →  dal.py (DAL)  →  MySQL (MRC)
```

| File | Layer | Responsibility |
|---|---|---|
| `app.py` | View (Flask) | Routes, session management, form handling, rendering templates |
| `bll.py` | Business Logic | Input validation, conflict checking, bridges View ↔ DAL |
| `dal.py` | Data Access | All SQL, stored procedure calls, DB connection lifecycle |
| `config.ini` | Configuration | Database credentials (not committed to version control) |
| `templates/` | HTML Templates | Jinja2 templates for each page |

---

## Prerequisites

- Python 3.10+
- MySQL 8.0+ with the MRC database set up using clarke_csc6302_database_principles_project_mod4+5 SQL file
- The following Python packages:

```bash
pip install flask mysql-connector-python pandas
```

---

## Configuration

Before running the app, create a `config.ini` file in the project root with your database credentials:

```ini
[Database]
host = localhost
user = your_mysql_username
port = 3306
database = mrc
password = your_mysql_password
```

> **Important:** Do not commit `config.ini` to version control. Add it to your `.gitignore`.

---

## Database Setup

Run the clarke_csc6302_database_principles_project_mod4+5 SQL file against your MySQL instance before starting the app:

```bash
mysql -u your_username -p < clarke_csc6302_database_principles_project_mod4+5.sql
```

This creates the `mrc` database with the `vessels`, `passengers`, and `trips` tables, the `All Trips` and `Total Revenue by Vessel` views, and all required stored procedures and functions.

---

## How to Run

### 1. Install dependencies

```bash
pip install flask mysql-connector-python pandas
```

### 2. Set up `config.ini` (see above)

### 3. Start the Flask server

```bash
python app.py
```

### 4. Open in your browser

```
http://127.0.0.1:5000
```

> **Entry point:** `app.py`  
> The app runs in debug mode by default. For production, set `debug=False` and use a proper WSGI server (e.g., gunicorn).

---

## Login Credentials

```
Username: admin
Password: secret
```

Sessions are maintained using Flask's `session` object with a secret key. Logging out clears the session entirely.

---

## Application Pages and Routes

| Route | Method | Description |
|---|---|---|
| `/` | GET | Home page — shows username if logged in |
| `/login` | GET, POST | Login form with server-side validation |
| `/logout` | GET | Clears session and redirects to login |
| `/dashboard` | GET | Main menu (requires login) |
| `/add-passenger` | GET, POST | Form to add a new passenger |
| `/add-vessel` | GET, POST | Form to add a new vessel |
| `/add-trip` | GET, POST | Form to add a new trip with dropdowns and datetime picker |
| `/all-trips-view` | GET | Displays all trips from the `All Trips` view in a formatted table |

---

## Key Features

### Login & Session Management
Users must authenticate before accessing any data pages. The session stores the username and all protected routes redirect to `/login` if no active session exists.

### Add Trip Special Considerations
- **Double-booking prevention:** Before calling `addTrip`, the BLL checks for vessel conflicts (`check_vessel_conflict`) and passenger conflicts (`check_passenger_conflict`) at the same date and time. A clear error message is shown if either would result in a double booking.
- **Dropdowns:** The passenger and vessel selectors are populated dynamically from the live database at page load no hardcoded options.
- **Datetime picker:** The departure date and time use an HTML `datetime-local` input, split server-side into separate `date` and `time` values before being passed to the BLL.
- **Passenger value encoding:** Passengers are passed as `"first_name|last_name"` strings from the dropdown, then split in the route handler before being forwarded to the BLL.

### All Trips View
Displays the `All Trips` database view as an HTML table. Data is rendered using Jinja2 templating no raw tuples or Python type labels are shown to the user.

---

## Error Handling

| Scenario | Behavior |
|---|---|
| DB connection failure | `mysql.connector.Error` caught at startup; app will not start |
| Missing login fields | Server-side validation, error shown inline on login form |
| Invalid credentials | Error shown inline, no redirect |
| Missing form fields | Inline error on the relevant form page |
| Non-integer cost/trip length | Caught with `try/except`, error shown to user |
| Vessel double-booked | BLL raises `ValueError`, shown as form error |
| Passenger double-booked | BLL raises `ValueError`, shown as form error |
| Duplicate passenger/vessel | `addPassenger`/`addVessel` procedures skip silently; no crash |
| `addTrip` return codes | `-1` (no vessel), `-2` (no passenger), `-3` (neither), `0` (duplicate) handled in BLL |

---

## Project Structure

```
Clarke_MRCapplication/
├── app.py                  # Entry point — Flask view layer
├── bll.py                  # Business Logic Layer
├── dal.py                  # Data Access Layer
├── config.ini              # DB credentials (not committed to git)
├── clarke_csc6302_database_principles_project_mod4+5.sql     # Database setup script
├── templates/
│   ├── index.html          # Home page
│   ├── login.html          # Login form
│   ├── dashboard.html      # Main menu after login
│   ├── add_passenger.html  # Add passenger form
│   ├── add_vessel.html     # Add vessel form
│   ├── add_trip.html       # Add trip form (dropdowns + datetime picker)
│   └── view_all_trips.html # All trips table view
└── README.md               # This file
```

---

## Design Notes

**Config file over runtime prompts:** Moving credentials to `config.ini` allows the Flask server to establish its DB connection at startup rather than per-request, which is appropriate for a persistent web app.

**Conflict checking in the BLL:** Double-booking logic lives in `TripService.add_trip()` using two new DAL methods (`check_vessel_conflict`, `check_passenger_conflict`). These query the `trips` table using the existing `GETVESSELID` and `GETPASSENGERID` SQL functions, keeping the BLL free of direct SQL while leveraging the existing database functions.

**Passenger encoding:** Since HTML `<select>` values are strings, passengers are encoded as `"first_name|last_name"` in the dropdown value attribute and split on `|` in the route handler — a simple approach that avoids needing a separate ID lookup round-trip in the view layer.