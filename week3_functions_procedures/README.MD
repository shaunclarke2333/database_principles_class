# Merrimack River Cruises Functions and Procedures

**Course:** CSC6302 Database Principles  
**Module:** 03 Functions and Procedures  
**Author:** Shaun Clarke

---

## Project Overview

This module extends the MRC database by introducing **views**, **user-defined functions**, and **stored procedures**. The goal is to make the database more usable for non-technical staff providing human-readable reports through views, and safe, reusable insertion logic through procedures that guard against duplicate entries.

No changes were made to the underlying table structure.

---

## Features

- Two views for reporting: trip details and revenue summaries
- Two scalar functions for looking up IDs by name
- Three stored procedures for safely inserting passengers, vessels, and trips
- Duplicate-safe insertion logic using `NOT EXISTS` with the `DUAL` dummy table
- Date/time formatting for non-technical users via `DATE_FORMAT` and `TIMESTAMP`
- An ER diagram (uploaded separately as a PDF)

---

## Database Schema

**Database:** `MRC`

The three core tables (`vessels`, `passengers`, `trips`) remain unchanged from last week's code. Key fields:

**`vessels`** `ID` (PK), `Vessel`, `Cost_Per_Hour`  
**`passengers`** `ID` (PK), `First_Name`, `Last_Name`, `Street`, `City`, `State`, `ZIP`, `Phone`, `getsSeasick`  
**`trips`** composite PK on `(Vessel_ID, Date, Departure_Time)`, FK to `vessels` and `passengers`

---

## Views

### `All_Trips`
Displays one row per voyage with the following columns:

| Column | Description |
|---|---|
| `Date_and_Time` | Human-readable combined date and time (e.g., *March 1, 2025 09:00 AM*) |
| `Vessel_Name` | Name of the vessel |
| `Passenger_Name` | Full name (first + last concatenated) |
| `Passenger_Address` | Street, city, state, and ZIP concatenated |
| `Passenger_Phone` | Phone number |
| `Voyage_Length` | Duration in hours |
| `Amount_Paid` | Calculated as `Cost_Per_Hour × Length_in_Hours` |

Sorted by most recent voyage first.

### `Total_Revenue_by_Vessel`
Aggregates the `All_Trips` view to show total revenue per vessel, sorted highest to lowest. Uses `All_Trips` as its data source rather than querying the base tables directly.

---

## Functions

### `getVesselId(vNameInput)`
Returns the `ID` of a vessel by its name. Returns `-1` if no match is found.

```sql
SELECT getVesselId('Ocean Voyager');  -- returns 1
SELECT getVesselId('Ghost Ship');     -- returns -1
```

### `getPassengerId(passengerNameInput)`
Returns the `ID` of a passenger by their full name (first + last). Returns `-1` if no match is found.

```sql
SELECT getPassengerId('Emily Clark');  -- returns 1
SELECT getPassengerId('Jane Doe');     -- returns -1
```

---

## Stored Procedures

### `addPassenger`
Inserts a new passenger into the `passengers` table. If a passenger with the same first and last name already exists, the insert is skipped silently.

```sql
CALL addPassenger(6, 'Barry', 'Allen', '234 Star St', 'Central City', 'MA', '23456', '978-555-5678', NULL);
```

### `addVessel`
Inserts a new vessel into the `vessels` table. Skips the insert if a vessel with the same name already exists.

```sql
CALL addVessel(4, 'Wave Rider', 450.00);
```

### `addTrip`
Inserts a new trip using vessel and passenger **names** (not IDs). Internally calls `getVesselId` and `getPassengerId` to resolve the foreign keys. Skips the insert if a matching trip for that passenger and vessel already exists.

```sql
CALL addTrip('Wave Rider', 'Barry Allen', '2025-03-01', '09:00:00', 30.00, 4);
```

---

## Prerequisites

- [MySQL](https://www.mysql.com/downloads/) 8.0+
- MySQL Workbench or the MySQL command-line client

---

## How to Run

### Option 1: MySQL Command Line

```bash
mysql -u your_username -p < module03_clarke.sql
```

### Option 2: MySQL Workbench

1. Open MySQL Workbench and connect to your local MySQL server.
2. Go to **File > Open SQL Script** and select `module03_clarke.sql`.
3. Click the **Execute** (lightning bolt) button.
4. Output from `SELECT` calls and view queries will appear in the results tabs.

### Option 3: Source Command (Inside MySQL Shell)

```sql
SOURCE /path/to/module03_clarke.sql;
```

> **Note:** The script drops and recreates the `MRC` database it is safe to run multiple times.

---

## Design Notes

**Duplicate-safe inserts:** Rather than using `INSERT IGNORE` or `ON DUPLICATE KEY UPDATE`, all procedures use `INSERT INTO ... SELECT ... FROM DUAL WHERE NOT EXISTS(...)`. This approach works even when the new values don't yet exist in any table, since `DUAL` acts as a one-row dummy source.

**Timestamp sorting:** The `All_Trips` view orders results by `TIMESTAMP(t.date, t.departure_time)` rather than the formatted `Date_and_Time` string, since string ordering on formatted dates doesn't sort correctly chronologically.

**`addTrip` limitation:** The current implementation skips a trip insert if *any* trip exists for that passenger/vessel combination. This is appropriate for the dataset but could be relaxed for a production system where the same passenger might legitimately take multiple trips on the same vessel.

---

## File Structure

```
module03/
├── module03_clarke.sql   # Main SQL script
├── ER_Diagram.pdf        # Entity-relationship diagram (reverse engineered in MySQL Workbench)
└── README.md             # This file
```