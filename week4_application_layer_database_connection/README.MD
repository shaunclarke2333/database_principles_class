# Merrimack River Cruises – Application Layer

**Course:** CSC6302 – Database Principles  
**Module:** 04 – Application Layer  
**Author:** Shaun Clarke

---

## Project Overview

This module wraps the MRC MySQL database in a fully layered Python application using a classic **three-tier architecture**: a View layer for user interaction, a Business Logic Layer (BLL) for orchestration and validation, and a Data Access Layer (DAL) for all database communication. No SQL appears outside of the DAL.

The application connects to a live MySQL database at runtime, prompts the user for credentials, and demonstrates reading views, calling functions, and executing stored procedures all formatted for a non-technical audience.

---

## Architecture

```
view.py  →  bll.py  →  dal.py  →  MySQL (MRC database)
```

| File | Layer | Responsibility |
|---|---|---|
| `view.py` | View | Entry point. Prompts for DB credentials, orchestrates output, formats data for display |
| `bll.py` | Business Logic Layer | Input validation, error handling, bridges View ↔ DAL |
| `dal.py` | Data Access Layer | All SQL queries, stored procedure calls, and DB connection management |

---

## Prerequisites

- Python 3.10+
- MySQL 8.0+ with the MRC database set up from Module 03
- The following Python packages:

```bash
pip install mysql-connector-python pandas
```

---

## How to Run

### 1. Set up the database
Make sure you have run `module03_clarke.sql` against your MySQL instance first. The application depends on the `vessels`, `passengers`, and `trips` tables, the `All Trips` and `Total Revenue by Vessel` views, and the `getVesselId`, `getPassengerId`, `addPassenger`, `addVessel`, and `addTrip` stored routines.

### 2. Install dependencies

```bash
pip install mysql-connector-python pandas
```

### 3. Run the application

```bash
python view.py
```

> **Entry point:** `view.py`

### 4. Enter your database credentials when prompted

The application will prompt for the following input is hidden for security:

```
Host:
User:
Port:
Database:
Password:
```

Typical local values: host `localhost`, port `3306`, database `mrc`.

---

## What the Application Does

Once connected, the application runs the following sequence automatically:

**1. Total Revenue by Vessel** queries the `Total Revenue by Vessel` view and displays results as a formatted table using pandas.

**2. Vessel ID lookup (match)** calls `getVesselId` with `"Ocean Voyager"` and prints the returned ID.

**3. Vessel ID lookup (no match)** calls `getVesselId` with `"Big Boat"` and confirms that `-1` is returned when no vessel is found.

**4. Add a new trip** calls `addPassenger`, `addVessel`, and `addTrip` stored procedures in sequence to insert:
- Passenger: Barry Allen, phone `212-312-4567`
- Vessel: Wave Rider, $150/hr
- Trip: Wave Rider / Barry Allen, June 30 2025 at noon, 3 hours, 5 passengers

Duplicate-safe: re-running the application will not create duplicate records.

**5. All Trips view** queries the `All Trips` view and displays all trips including the newly added one, formatted with human-readable dates and times.

---

## Project Structure

```
Clarke_MRCapplication/
├── view.py       # Entry point — View layer
├── bll.py        # Business Logic Layer
├── dal.py        # Data Access Layer
└── README.md     # This file
```

---

## Layer Details

### DAL (`dal.py`)
- `ManageDbConnection` handles connect, disconnect, cursor lifecycle, and commit
- `DatabaseActions` generic `select_query` and `procedure_calls` wrappers
- `VesselsDal` `get_all_rows`, `get_vessel_id`, `add_vessel_proc`, `get_total_rev_view`
- `PassengersDal` `get_all_rows`, `get_passenger_id`, `add_passenger_proc`
- `TripsDal` `get_all_rows`, `add_trip_proc`, `get_all_trips_view`

### BLL (`bll.py`)
- `VesselService` validates vessel name and cost, delegates to `VesselsDal`
- `PassengerService` validates passenger name and phone, delegates to `PassengersDal`
- `TripService` validates all trip fields, interprets return codes (`-1`, `-2`, `-3`, `0`, `True`) from `addTrip`
- `MRCAppService` single entry point for all View-layer calls, composes the three services above

### View (`view.py`)
- Prompts for credentials using `getpass` (input not echoed to terminal)
- Formats all query output as pandas DataFrames (no raw tuples or quotes)
- Handles `addTrip` result codes and prints a plain-English status message

---

## Error Handling

| Scenario | Behavior |
|---|---|
| DB connection failure | `mysql.connector.Error` caught and printed |
| Vessel not found | `getVesselId` returns `-1`; BLL and View surface a clear message |
| Passenger not found | `getPassengerId` returns `-1`; similarly surfaced |
| Duplicate passenger or vessel | `addPassenger`/`addVessel` silently skip; no crash |
| `addTrip` errors | Return codes `-1` (no vessel), `-2` (no passenger), `-3` (neither), `0` (duplicate) are each handled with a distinct message |