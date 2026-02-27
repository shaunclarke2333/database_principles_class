# Merrimack River Cruises – Database Creation and Setup

**Course:** CSC6302 – Database Principles  
**Module:** 01 – Databases and DBMS  
**Author:** Shaun Clarke

---

## Project Overview

This project involves designing and setting up a relational database for **Merrimack River Cruises (MRC)**, a local business that previously tracked customer reservations in a spreadsheet. The goal was to migrate that data into a structured MySQL database with proper schema design, data insertion, and querying.

---

## Features

- Drops and recreates the `MRC` database from scratch on each run (idempotent setup)
- Creates a `Reservations` table with correctly typed attributes mirroring the original CSV columns
- Inserts the first six rows of reservation data manually via `INSERT` statements
- Includes four `SELECT` queries — one full table query and three filtered queries using `WHERE` clauses

---

## Database Schema

**Database:** `MRC`  
**Table:** `Reservations`

| Column | Data Type | Notes |
|---|---|---|
| `Date` | `DATE` | Date of the voyage |
| `Departure_Time` | `TIME` | Time of departure |
| `Length_in_Hours` | `DECIMAL(4,2)` | Duration of the cruise |
| `Vessel` | `CHAR(20)` | Name of the vessel |
| `First_Name` | `CHAR(20)` | Customer first name |
| `Last_Name` | `CHAR(20)` | Customer last name |
| `Street` | `VARCHAR(50)` | Street address |
| `City` | `CHAR(20)` | City |
| `State` | `CHAR(6)` | State abbreviation |
| `ZIP` | `VARCHAR(10)` | ZIP code (leading zeros preserved) |
| `Phone` | `VARCHAR(50)` | Phone number |
| `Total_Passengers` | `INT` | Number of passengers |
| `Total_Cost` | `DECIMAL(19,2)` | Total reservation cost |

---

## Prerequisites

- [MySQL](https://www.mysql.com/downloads/) 8.0+ (or compatible MariaDB)
- MySQL command-line client or a GUI tool like [MySQL Workbench](https://www.mysql.com/products/workbench/)

---

## How to Run

### Option 1: MySQL Command Line

```bash
mysql -u your_username -p < module01_clarke.sql
```

You will be prompted for your password. The script will drop and recreate the `MRC` database, create the table, insert the data, and run all SELECT queries.

### Option 2: MySQL Workbench

1. Open MySQL Workbench and connect to your local MySQL server.
2. Go to **File > Open SQL Script** and select `module01_clarke.sql`.
3. Click the lightning bolt (**Execute**) button to run the entire script.
4. Results for all `SELECT` queries will appear in the output panel.

### Option 3: Source Command (Inside MySQL Shell)

```sql
SOURCE /path/to/module01_clarke.sql;
```

---

## Queries Included

The script runs the following queries after inserting data:

1. **All reservations** — retrieves every row and column from the table.
2. **Customers named John** — returns first and last name for all records where `First_Name = 'John'`.
3. **Customers at 456 Pine St** — returns name and full address for records matching that street.
4. **Groups of 3 passengers** — returns name and passenger count for reservations with exactly 3 passengers.

---

## File Structure

```
module01/
├── module01_clarke.sql   # Main SQL script (schema + data + queries)
└── README.md             # This file
```

---

## Notes

- ZIP codes that were missing a leading zero in the original CSV have been corrected (e.g., `01234`).
- The script is fully idempotent — running it multiple times will always produce a clean, consistent database state thanks to `DROP DATABASE IF EXISTS`.