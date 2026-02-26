# MBD Wellness Application

**Author:** Shaun Clarke  
**Class:** CSC6302 – Database Principles  
**Module:** 08 – Final Project  

---

## 1. Project Overview

This project is a **Flask-based wellness tracking application** that allows users to:

- Create an account and authenticate
- Log meals, workouts, and weight entries
- View a personalized dashboard with advanced data visualizations
- Track historical workout and weight data

The application follows a layered architecture using:

- Flask (Application Layer)
- BLL (Business Logic Layer)
- DAL (Data Access Layer)
- MySQL (Database Layer)

---

## 2. Advanced Features

### Dashboard Data Visualizations (Advanced Feature)

The dashboard includes two advanced visualizations built with **Plotly Express**:

#### Macro Distribution Pie Chart
- Displays Protein, Carbs, and Fats (grams)
- Automatically shows the latest available day
- Gracefully handles users with no data by showing a placeholder chart

#### Weight Trend Line Chart
- Displays the user’s weight over time
- Sorted chronologically
- Includes markers for clarity
- Shows a placeholder chart if no weight data exists

These charts are dynamically generated using **Pandas aggregation** and rendered in the dashboard using **Plotly HTML output**.

---

## 3. Requirements

All required Python packages are listed in the `requirements.txt` file.

Install dependencies with:

```bash
pip install -r requirements.txt
```

---

## 4. Database Configuration

**Database Name:**
```
mbd
```

**Database Credentials (for testing):**
```
Username: root
Password: N@thin23:
Host: localhost
Port: 3306
```

---

## 5. Test User (Already Created)

You may use the following test account to immediately access the dashboard  
(feel free to create your own account as well):

```
Username: shaunc
Password: hash_shaun_123
```

---

## 6. How to Run the Application

### Step 1: Start MySQL
Ensure your MySQL server is running and the `mbd` database exists.

---

### Step 2: Install Dependencies
From the project root directory:

```bash
pip install -r requirements.txt
```

---

### Step 3: Run the Flask App

```bash
python app.py
```

The application will start at:

```
http://127.0.0.1:5000
```

---

## 7. Application Workflow

### 1. Connect to Database
- Click the **DB Connect** button in the navigation bar
- Enter:
  - Username: `root`
  - Password: `N@thin23:`
- The session will store the database connection state

---

### 2. Sign Up (Optional)
- Navigate to **Sign Up**
- Enter all required fields:
  - Name, username, email, password
  - Height, weight, DOB, gender
- Account is created using a stored procedure

---

### 3. Sign In
- Navigate to **Sign In**
- Enter username and password
- Successful login redirects to the dashboard

---

### 4. Log a Meal
- Navigate to **Create Meal**
- Enter:
  - Meal date/time
  - Meal type
  - Notes
- Add food items and servings
- Meal macros are calculated automatically

---

### 5. Log a Workout
- Navigate to **Log Workout**
- Select an exercise
- Enter:
  - Duration
  - Sets, reps, weight
- Recent workouts are displayed on the same page

---

### 6. View Dashboard (Advanced Feature)
- Navigate to **Dashboard**
- View:
  - Macro distribution pie chart (latest day)
  - Weight trend line chart
- Charts update automatically as data is logged

---

### 7. View Workout History
- Navigate to **Workout History**
- View all logged workouts in a table format

---

### 8. Log Weight
- Navigate to **Log Weight**
- Enter:
  - Weight
  - Date/time
- Recent entries are displayed

---

### 9. View Weight History
- Navigate to **Weight History**
- View all historical weight entries
