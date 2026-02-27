# CSC6302 – Database Principles

**Institution:** Merrimack College  
**Author:** Shaun Clarke  

---

## Overview

This repository contains all projects completed during **CSC6302 Database Principles**, a graduate-level course covering relational database design, normalization, SQL programming, and full-stack application development with a database backend.

The work progresses from foundational schema design through stored procedures and views, and culminates in a fully layered three-tier web application with interactive data visualizations. Each project builds directly on the one before it.

---

## Project Progression

```
Module 01 → Module 02 → Module 03 → Module 04 → Module 05 → Final Project
  Schema    Normalize   Procedures   Python CLI   Flask Web    Full App +
  & Data    & Joins     & Views      3-Tier App   GUI Layer    Charts
```

---

## Modules

### [Module 01 – Database Creation and Setup](./Module01/)
Designed and created a MySQL database for a fictional local business, **Merrimack River Cruises (MRC)**. Defined a schema from a raw CSV file, selected appropriate data types, inserted seed data, and wrote filtered `SELECT` queries.

**Skills:** Schema design, DDL, DML, data types, `WHERE` clauses

---

### [Module 02 – Normalization and Queries](./Module02/)
Decomposed the flat `Reservations` table into three normalized tables (`Vessels`, `Passengers`, `Trips`) using only SQL built-in functions. Designed a composite primary key for the `Trips` table and documented the superkey and candidate key analysis in comments. Reconstructed the original view using a multi-table `JOIN`.

**Skills:** 3NF normalization, composite keys, foreign keys, `INSERT INTO ... SELECT`, multi-table joins

---

### [Module 03 – Functions and Procedures](./Module03/)
Extended the MRC database with views for reporting, scalar functions for ID lookups, and stored procedures for safe data insertion. All procedures handle duplicate records and missing references gracefully using `NOT EXISTS` and `DUAL`.

**Skills:** Views, user-defined functions, stored procedures, duplicate-safe inserts, `DATE_FORMAT`, aggregate queries

---

### [Module 04 – Python Application Layer (CLI)](./Module04/)
Wrapped the MRC database in a Python three-tier application. The CLI view layer prompts for database credentials at runtime, calls BLL methods for validation and orchestration, and the DAL handles all SQL via `mysql-connector-python`.

**Skills:** Python, three-tier architecture, `mysql-connector-python`, stored procedure calls, input validation, pandas DataFrames

---

### [Module 05 – Flask Web Application](./Module05/)
Replaced the CLI view with a Flask web application. Added session-based login, HTML forms with server-side validation, dropdown-populated trip booking, and a datetime picker. Double-booking prevention logic was added to the BLL. Database credentials are loaded from `config.ini`.

**Skills:** Flask, Jinja2 templates, sessions, form handling, config files, double-booking conflict detection

---

### [Final Project – Mind Body Dashboard](./FinalProject/)

A full-stack personal health and wellness tracking application built from scratch across three phases.

| Phase | Deliverable |
|---|---|
| Part 1 – Planning | ER diagram and schema design for a 10-table wellness database |
| Part 2 – Database | Full MySQL database with views, functions, and stored procedures covering CRUD + cascades |
| Part 3 – Application | Flask web app with workout, nutrition, weight, and mood logging — plus interactive Plotly dashboard charts as the advanced feature |

**Advanced Feature:** Interactive **Plotly** charts on the user dashboard a macros breakdown pie chart and a weight trend line chart — both generated live from database views and rendered in the browser without a page refresh.

**Skills:** Full-stack development, Flask, Plotly, pandas, multi-table schema design, session management, layered architecture, data visualization

---

## Technologies Used

| Category | Tools |
|---|---|
| Database | MySQL 8.0 |
| Backend | Python 3.10+, Flask |
| Database Driver | `mysql-connector-python` |
| Data Processing | `pandas` |
| Data Visualization | `plotly` |
| Templating | Jinja2 |
| Design Pattern | Three-tier architecture (View → BLL → DAL) |

---

## Repository Structure

```
CSC6302-Database-Principles/
├── Module01/
│   ├── module01_clarke.sql
│   └── README.md
├── Module02/
│   ├── module02_clarke.sql
│   └── README.md
├── Module03/
│   ├── module03_clarke.sql
│   ├── ER_Diagram.pdf
│   └── README.md
├── Module04/
│   ├── view.py
│   ├── bll.py
│   ├── dal.py
│   └── README.md
├── Module05/
│   ├── app.py
│   ├── bll.py
│   ├── dal.py
│   ├── config.ini          ← not committed
│   ├── templates/
│   └── README.md
└── FinalProject/
    ├── Part1/
    │   ├── Clarke_FinalProject_ERD.pdf
    │   └── README.md
    ├── Part2/
    │   ├── Clarke_FinalProject_Part2.sql
    │   └── README.md
    └── Part3/
        ├── app.py
        ├── bll.py
        ├── dal.py
        ├── Clarke_FinalProject_Part3.sql
        ├── templates/
        └── README.md
```

---

## Running Any Project

Each module folder contains its own `README.md` with specific setup and run instructions. The general pattern is:

**SQL projects (Modules 01–03):**
```bash
mysql -u your_username -p < module_file.sql
```

**Python/Flask projects (Modules 04–05, Final Project):**
```bash
pip install flask mysql-connector-python pandas plotly
python app.py   # or view.py for Module 04
```

Then open `http://127.0.0.1:5000` in your browser.

> All SQL scripts are idempotent — they drop and recreate the database each run, so they are safe to execute multiple times.