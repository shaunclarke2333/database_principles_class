# MRC Application – Project Requirements

This document outlines the requirements and structure for the **MRC Application** assignment.  
Follow all steps carefully to ensure proper organization and functionality.

---

## 1. Choose Your Programming Language
Select one of the following languages to develop your application:

- Python  
- Java  
- JavaScript  

If you prefer another language, contact the instructor for approval.

---

## 2. Project Folder Structure
Create a folder named:
- <lastname>_MRCapplication

This folder must contain:

- View layer  
- Business Logic Layer (BLL)  
- Data Access Layer (DAL)  
- README file  

---

## 3. Required Files and Layer Responsibilities
Your application should include at least **three files**:

- `View.py`  
- `BLL.py`  
- `DAL.py`  

You may use a more advanced structure if you have prior experience, but the following rules apply:

- The **View** imports and calls methods in the **BLL**.  
- The **BLL** imports and calls methods in the **DAL**.  
- The **DAL** contains all code interacting with the database.  
- **No SQL** may appear in the View or BLL.

---

## 4. Data Access Layer (DAL) Requirements

### 4a. Database Connectivity
Your DAL must include:

- A method or class to establish and close database connections  
- A cursor manager  
- Commit logic (when needed)  

A custom connection class is allowed but not required.

### 4b. Table Classes
Create **one class per table** (three total).  
Each class must contain at least **two methods**:

- A method to read data  
- A method to add data  

These should utilize the stored procedures and functions provided in the starter SQL file.  
Your BLL layer will pass the required parameters to these DAL methods.

---

## 5. Business Logic Layer (BLL) Requirements
Your BLL must:

- Act as a bridge between the View and DAL  
- Contain classes or functions that orchestrate application flow  
- Call the appropriate DAL methods  
- Accept arguments from the View when required  

Each BLL method should map to one or more DAL methods.

---

## 6. View Layer Requirements
Your View should provide:

- Clear display of information  
- A logical scaffold that runs from start to finish  
- User prompts for database connection details  

The View must perform the following:

### 6a. Prompt for DB Credentials
Collect database host, username, password, database name, and port from the user, then initiate the connection.

### 6b. Display "Total Revenue by Vessel"
Call the appropriate view and format the results in a user-friendly way:

- No tuples  
- Strings should not contain quotes  
- Dates, times, and currency must be formatted for non-technical users  

### 6c. Call `getVesselID` Twice
- Once with a matching vessel  
- Once where no match is found  
- Display both results cleanly

### 6d. Add a New Trip
Call the `addTrip` stored procedure to insert:

- A new vessel  
- A new passenger  
- A new trip  

You may need to call supporting stored procedures first.  
Ensure that all inserts are committed to the database.

### 6e. Display "All Trips"
Call the "All Trips" view and show the results in a user-friendly format.  
The newly added trip must be visible.

---

## 7. README Instructions
Your final **README.md** must explain:

- How to run your program  
- Any dependencies or commands needed  
- Which file acts as the entry point (default assumption: `Main.py` or `View.py`)  

Provide clear instructions so the grader can execute your program without guessing.
