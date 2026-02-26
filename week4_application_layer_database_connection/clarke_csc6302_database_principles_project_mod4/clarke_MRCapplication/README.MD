# MRC Application – Run Instructions

Author: Shaun Clarke  
Class: CSC6302 Database Principles  
Module 04: Application Layer  

## 1. Prerequisites

### 1.1. Software

- **Python** 3.10+ installed and available on your PATH  
- **MySQL Server** installed and running  
- Access to a MySQL user with permission to:
  - Create tables / views  
  - Create and execute stored procedures and functions  
  - Insert / select data  

### 1.2. Python Packages

Install the required packages using:

pip install:
mysql-connector-python
pandas
getpass

These are required for MySQL connectivity and for displaying data in table format.

## 2. Running the Program

To run the application:

### 2.1 Open your terminal and navigate into the project directory:

- cd clarke_MRCapplication
- You must be inside this directory, because the View imports the BLL and DAL from the same folder.

### 2.2 Run the main program:

- python view.py
- (Use python3 instead of python if required on your system.)

### 2.3 When prompted, enter the database connection information:

- Host
- User
- Port
- Database
- Password

After this, the program will run automatically from start to finish—displaying revenue, looking up vessel IDs, inserting a new trip, and showing the updated trip view.