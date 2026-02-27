# Merrimack River Cruises Normalization and Queries

**Course:** CSC6302 Database Principles  
**Module:** 02 Normalization and Queries  
**Author:** Shaun Clarke

---

## Project Overview

Building on the MRC database from Module 01, this project applies **database normalization** to decompose the flat `Reservations` table into three well structured relational tables: `Vessels`, `Passengers`, and `Trips`. The decomposition eliminates redundancy, improves data integrity, and sets up proper primary/foreign key relationships. All data migration is handled entirely using SQL built-in functions no manual re-entry.

---

## What Changed From Module 01

The original `Reservations` table stored everything in one flat structure, causing repeated customer and vessel data across rows. This module splits that data into:

- **Vessels** unique boats and their calculated hourly rate
- **Passengers** unique customer records with contact/address info
- **Trips** each booking event, linking a passenger to a vessel on a specific date/time

---

## Database Schema

**Database:** `MRC`

### `Reservations` (unchanged — source table)
The original flat table provided by the starter code. Not modified.

---

### `Vessels`

| Column | Data Type | Notes |
|---|---|---|
| `vessel_id` | `INT AUTO_INCREMENT` | Primary key |
| `vessel_name` | `VARCHAR(50)` | Name of the boat |
| `cost_per_hour` | `DECIMAL(6,2)` | Derived from `Total_Cost / Length_in_Hours` via SQL |

---

### `Passengers`

| Column | Data Type | Notes |
|---|---|---|
| `passenger_id` | `INT AUTO_INCREMENT` | Primary key |
| `first_name` | `VARCHAR(50)` | |
| `last_name` | `VARCHAR(50)` | |
| `street` | `VARCHAR(50)` | |
| `city` | `VARCHAR(50)` | |
| `state` | `CHAR(2)` | |
| `zip` | `CHAR(5)` | |
| `phone` | `CHAR(12)` | |

---

### `Trips` (Composite Primary Key)

| Column | Data Type | Notes |
|---|---|---|
| `date` | `DATE` | Part of composite PK |
| `departure_time` | `TIME` | Part of composite PK |
| `length_in_hours` | `DECIMAL(4,2)` | |
| `vessel_id` | `INT` | FK → `Vessels`, part of composite PK |
| `passenger_id` | `INT` | FK → `Passengers`, part of composite PK |
| `total_passengers` | `INT` | |

**Primary Key:** `(date, vessel_id, departure_time, passenger_id)`

#### Key Analysis (documented in SQL comments)
- **Total superkeys:** 4
- **Candidate keys:**
  - `(date, vessel_id, departure_time, passenger_id)`
  - `(date, vessel_id, departure_time, total_passengers)`
- **Chosen PK:** `(date, vessel_id, departure_time, passenger_id)` this combination uniquely identifies each trip while establishing a meaningful foreign key relationship to the `Passengers` table, directly tying a specific customer to a specific vessel at a specific time.

---

## Prerequisites

- [MySQL](https://www.mysql.com/downloads/) 8.0+ (or compatible MariaDB)
- MySQL Workbench or the MySQL command-line client

---

## How to Run

### Option 1: MySQL Command Line

```bash
mysql -u your_username -p < module02_clarke.sql
```

### Option 2: MySQL Workbench

1. Open MySQL Workbench and connect to your local MySQL server.
2. Go to **File > Open SQL Script** and select `module02_clarke.sql`.
3. Click the **Execute** (lightning bolt) button.
4. Results for all `SELECT` queries will appear in the output tabs.

### Option 3: Source Command (Inside MySQL Shell)

```sql
SOURCE /path/to/module02_clarke.sql;
```

> **Note:** The script drops and recreates the `MRC` database at the top it is fully idempotent and safe to run multiple times.

---

## Queries Included

The script runs the following queries:

1. `SELECT * FROM passengers` — all unique customer records
2. `SELECT * FROM vessels` — all vessels with their calculated hourly cost
3. `SELECT * FROM trips` — all trip records with FK references
4. **Reconstruction join** — joins all three tables to produce output matching `SELECT * FROM Reservations ORDER BY Date, Departure_Time ASC`, including a recalculated `total_cost` column using `length_in_hours * cost_per_hour`

---

## Design Decisions

**Cost Per Hour:** Rather than storing `Total_Cost` redundantly on every trip, a `cost_per_hour` rate is stored once per vessel and derived from the source data using `total_cost / length_in_hours`. Total cost is then reconstructed at query time via multiplication.

**No surrogate key on Trips:** The assignment required a composite primary key instead of a simple auto-increment ID. The combination of date, departure time, vessel, and passenger is semantically meaningful and guarantees uniqueness across the dataset.

**Data migration via SQL only:** All `INSERT INTO ... SELECT DISTINCT` statements use joins and SQL functions no hardcoded values were re-entered manually.

---

## File Structure

```
module02/
├── module02_clarke.sql   # Main SQL script
└── README.md             # This file
```