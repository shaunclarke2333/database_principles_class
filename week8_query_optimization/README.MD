# Mind Body Dashboard (MBD) Final Project

**Course:** CSC6302 Database Principles  
**Final Project Full Application Submission**  
**Author:** Shaun Clarke

---

## Project Overview

The **Mind Body Dashboard** is a personal health and wellness tracking web application built with Flask, MySQL, and Plotly. Users can log workouts, meals and nutrition, weight, and mood all tied to a personal account. The dashboard surfaces that data as interactive charts so users can see their progress at a glance.

This project represents the culmination of the course: a fully layered three-tier application with a graphical web UI, session-based authentication, database-backed CRUD operations, and an advanced data visualization feature.

---

## Advanced Feature: Interactive Dashboard Charts

The dashboard uses **Plotly** to render two live, interactive charts from the database:

- **Macros Pie Chart** shows the protein/carbs/fat breakdown (in grams) for the most recently logged day. Updates in real time as new meals are added.
- **Weight Trend Line Chart** plots all weight log entries over time for the logged-in user, with markers on each data point.

Both charts are generated server-side from database views, converted to HTML via `plotly.express`, and injected directly into the Jinja2 template. If a user has no data yet, placeholder charts are shown with a "No data yet" label rather than crashing. This feature required independent research into the Plotly Express and pandas libraries, which were not covered in coursework.

---

## Architecture

```
Browser  →  app.py (Flask View)  →  bll.py (Business Logic)  →  dal.py (DAL)  →  MySQL (mbd)
```

| File | Layer | Responsibility |
|---|---|---|
| `app.py` | View (Flask) | Routes, session management, form handling, chart rendering, Jinja2 templates |
| `bll.py` | Business Logic | Input validation, error handling, bridges View ↔ DAL |
| `dal.py` | Data Access | All SQL queries, stored procedure/function calls, DB connection lifecycle |
| `templates/` | HTML Templates | Jinja2 templates for every page |

**No SQL appears in `app.py` or `bll.py`.** The DAL uses only predefined stored procedures, functions, and views from the `mbd` database.

---

## Prerequisites

- Python 3.10+
- MySQL 8.0+ with the `mbd` database loaded
- The following Python packages:

```bash
pip install flask mysql-connector-python pandas plotly
```

---

## Database Setup

Run the final project SQL file against your MySQL instance before starting the application:

```bash
mysql -u your_username -p < Clarke_FinalProject_Part3.sql
```

This creates the `mbd` database with all tables, seed data, views, functions, and stored procedures. The script is idempotent — it drops and recreates the database each run.

---

## How to Run

### 1. Install dependencies

```bash
pip install flask mysql-connector-python pandas plotly
```

### 2. Start the Flask server

```bash
python app.py
```

### 3. Open in your browser

```
http://127.0.0.1:5000
```

> **Entry point:** `app.py`  
> The app runs in debug mode by default (`debug=True`). For any non-development use, set `debug=False`.

---

## Connecting to the Database

Database credentials are **not hardcoded**. On first load, click the **DB** button in the navbar to open the connection dialog. Enter your MySQL username and password. The host is defaulted to `localhost` and the port to `3306` both can be changed in the connection class if needed.

Once connected, credentials are stored in the Flask session for the duration of the browser session. The database name (`mbd`) is the only value that is fixed in code.

---

## Default Login

After connecting to the database, navigate to `/signin`. Use any seeded user account, for example:

```
Username: ShaunC
Password: hash_shaun_123
```

Or create a new account at `/signup`.

---

## Application Pages and Features

### Authentication
| Route | Description |
|---|---|
| `/` | Home page |
| `/signin` | Login form — validates credentials via `validateUser` stored procedure |
| `/signup` | Registration form — creates account via `createUser` stored procedure |
| `/logout` | Clears session |
| `/forgot-password` | Password reset via `resetPassword` stored procedure |
| `/delete-account` | Deletes account and all related data via `deleteAccount` (cascades) |

### Dashboard
| Route | Description |
|---|---|
| `/dashboard` | Displays Plotly macros pie chart and weight trend line chart for the logged-in user |

### Workouts
| Route | Description |
|---|---|
| `/workout/log` | Log a new workout session; shows 10 most recent sessions in a table |
| `/workout/history` | Full workout history for the logged-in user |

### Nutrition
| Route | Description |
|---|---|
| `/meals/create` | Create a new meal (type, date/time, notes); shows today's food items |
| `/meals/<id>/items` | Add food items and servings to an existing meal via dropdown |

### Weight
| Route | Description |
|---|---|
| `/weight/log` | Log a new weight entry; shows 10 most recent entries |
| `/weight/history` | Full weight history for the logged-in user |

### Account
| Route | Description |
|---|---|
| `/account` | Account settings page |

---

## CRUD Coverage

| Operation | Where |
|---|---|
| **Create** | Sign up, log workout, log mood, create meal, add meal item, log weight |
| **Read** | Dashboard charts, workout history, weight history, meal items table, all views |
| **Update** | Reset password (`resetPassword` procedure with cascade) |
| **Delete** | Delete account (`deleteAccount` procedure — cascades to all related tables) |

---

## Layer Details

### DAL (`dal.py`)

- `ManageDbConnection` connect, disconnect, cursor lifecycle
- `DatabaseActions` generic `select_query` and `procedure_calls` wrappers
- `UserChartsDal` queries `dailyMoodTrends`, `workoutSummaries`, `caloriesPerDaySummaries`, `dailyWeightSummary` views filtered by username
- `UsersDal` `validateUser`, `createUser`, `resetPassword`, `deleteAccount` procedures; user detail queries
- `ExerciseDal` reads `exercises` reference table for dropdown
- `FoodDal` reads `food` reference table for dropdown
- `MealsDal` `addMeal` procedure; meal lookup by ID and user
- `MealItemsDal` `addMealItem` procedure; today's items query; items-per-meal query
- `WeightLogsDal` `logWeight` procedure; recent and full weight history queries
- `WorkoutSessionsDal` `logWorkout` procedure; recent and full workout history queries
- `MoodEntriesDal` `logMood` procedure

### BLL (`bll.py`)

One service class per DAL class, each responsible for input validation before forwarding calls:

- `UserService` validates credentials, interprets return codes (`-1`, `-2`, `0`), validates signup fields
- `UserChartsService` fetches all four chart data sources for the dashboard
- `ExerciseService` / `FoodService` pass-through reads for dropdown population
- `MealsService` / `MealItemsService` validates servings > 0, resolves meal IDs
- `WeightLogService` validates weight is numeric; provides recent and full history methods
- `WorkoutSessionService` validates numeric fields (duration, sets, reps, weight); provides recent and full history methods
- `MoodEntriesService` validates mood/energy/stress scores are integers between 1–10

### View (`app.py`)

- `@deb_required` decorator redirects to home with a flash message if DB is not connected
- DB connection via `/db/connect` JSON endpoint credentials stored in Flask session
- All form handlers follow the pattern: validate → call BLL → interpret result code → flash message → redirect or re-render with inline error
- Dashboard route builds DataFrames from DB view data, generates Plotly charts, converts to HTML for Jinja2 injection

---

## Error Handling

| Scenario | Behavior |
|---|---|
| DB not connected | `@deb_required` decorator redirects to home with flash warning |
| Invalid DB credentials | `/db/connect` returns JSON `ok=False` with message |
| Invalid login | Flash message on signin page |
| Duplicate username at signup | Procedure returns `-1`; inline error shown |
| Duplicate email at signup | Procedure returns `-2`; inline error shown |
| Email/username mismatch on reset | Procedure returns `-3`; inline error shown |
| User not found on delete | Procedure returns `-1`; flash danger message |
| Exercise not found on workout log | Procedure returns `-1`; BLL raises exception; flash shown |
| Food not found on meal item add | Procedure returns `-1`; flash shown |
| Non-numeric form inputs | `try/except ValueError` in route; flash warning |
| Empty dashboard (no data yet) | Placeholder Plotly charts rendered with "No data yet" label |
| Any uncaught exception | `except Exception as e` in every route; flash with error string |

---

## File Structure

```
Clarke_FinalProject/
├── app.py                          # Entry point — Flask view layer
├── bll.py                          # Business Logic Layer
├── dal.py                          # Data Access Layer
├── Clarke_FinalProject_Part3.sql   # Database setup script
├── templates/
│   ├── home.html
│   ├── signin.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── forgot_password.html
│   ├── delete_account.html
│   ├── account_settings.html
│   ├── workout_log.html
│   ├── workout_history.html
│   ├── meal_create.html
│   ├── meal_add_items.html
│   ├── weight_log.html
│   └── weight_history.html
└── README.md                       # This file
```

---

## Dependencies

| Package | Purpose |
|---|---|
| `flask` | Web framework, routing, sessions, templating |
| `mysql-connector-python` | MySQL database driver |
| `pandas` | DataFrame construction for chart data processing |
| `plotly` | Interactive chart generation (advanced feature) |