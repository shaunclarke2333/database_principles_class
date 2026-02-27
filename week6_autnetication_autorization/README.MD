# Health & Wellness Tracker Final Project Part 1: Planning

**Course:** CSC6302 Database Principles  
**Module:** Final Project Part 1 (Planning Phase)  
**Author:** Shaun Clarke

---

## Project Overview

This document covers the planning phase for the **Health & Wellness Tracker** a personal health tracking application that allows users to log workouts, meals, mood, habits, and goals in a unified database. The planning phase includes the entity-relationship diagram and database design decisions that will carry through into Parts 2 and 3.

---

## Application Description

The Health & Wellness Tracker lets users:

- Log **workout sessions** (exercise, duration, sets, reps, weight)
- Track **nutrition** by logging meals and individual food items with macronutrient data
- Record daily **mood**, energy, and stress levels
- Set and monitor **goals** (weight, fitness, habit-based)
- Track recurring **habits** with daily completion logs
- Maintain a personal **profile** with biometric data

---

## Entity-Relationship Diagram

The ERD was designed and submitted separately as a PDF. The diagram shows all tables, primary keys, foreign keys, and cardinality relationships.

**ERD File:** `Clarke_FinalProject_ERD.pdf`

---

## Database Schema Summary

The database consists of **10 tables**:

### `users`
Central table. Stores account credentials and profile data (name, email, DOB, height, weight, gender).

| Key Fields | Type |
|---|---|
| `user_id` | `INT AUTO_INCREMENT` (PK) |
| `email` | `VARCHAR(150) UNIQUE` |
| `password_hash` | `VARCHAR(255)` |
| `date_of_birth` | `DATE` |
| `height` / `weight` | `DECIMAL(5,2)` |
| `gender` | `ENUM` |

---

### `workout_sessions`
Logs individual exercise sessions per user.

| Key Fields | Type |
|---|---|
| `session_id` | `INT AUTO_INCREMENT` (PK) |
| `user_id` | FK → `users` |
| `exercise_id` | FK → `exercises` |
| `session_datetime` | `DATETIME` |
| `sets`, `reps` | `INT NULL` |
| `weight` | `DECIMAL(6,2) NULL` |

---

### `exercises`
Reference table for exercise types (no FK — looked up by workout sessions).

| Key Fields | Type |
|---|---|
| `exercise_id` | `INT AUTO_INCREMENT` (PK) |
| `exercise_name` | `VARCHAR(100)` |
| `exercise_category` | `VARCHAR(50)` |
| `muscle_group` | `VARCHAR(50)` |

---

### `meals`
Logs meal events per user (breakfast, lunch, dinner, snack).

| Key Fields | Type |
|---|---|
| `meal_id` | `INT AUTO_INCREMENT` (PK) |
| `user_id` | FK → `users` |
| `meal_datetime` | `DATETIME` |
| `meal_type` | `ENUM('breakfast','lunch','dinner','snack')` |

---

### `food`
Reference table of food items with nutritional data.

| Key Fields | Type |
|---|---|
| `food_id` | `INT AUTO_INCREMENT` (PK) |
| `food_name` | `VARCHAR(100)` |
| `calories_per_serving` | `INT` |
| `protein` / `carbs` / `fat` | `DECIMAL(6,2)` |

---

### `meal_items`
Junction table linking meals to food items. Stores quantity (servings).

| Key Fields | Type | Notes |
|---|---|---|
| `meal_item_id` | `INT AUTO_INCREMENT` (PK) | |
| `meal_id` | FK → `meals` | |
| `food_id` | FK → `food` | |
| `servings` | `DECIMAL(5,2)` | Used to scale macros |

> **Composite key candidate:** `(meal_id, food_id)` uniquely identifies each food entry within a meal and will be used as a composite key in Part 2.

---

### `mood_entries`
Daily mood logs per user with optional energy/stress scores and a free-text note.

| Key Fields | Type |
|---|---|
| `mood_id` | `INT AUTO_INCREMENT` (PK) |
| `user_id` | FK → `users` |
| `entry_datetime` | `DATETIME` |
| `mood_score` | `TINYINT` |
| `energy_level` / `stress_level` | `TINYINT NULL` |

---

### `goals`
User-defined targets (e.g., lose 10 lbs, run 5K, drink 8 glasses of water daily).

| Key Fields | Type |
|---|---|
| `goal_id` | `INT AUTO_INCREMENT` (PK) |
| `user_id` | FK → `users` |
| `goal_type` | `VARCHAR(50)` |
| `target_value` | `DECIMAL(10,2)` |
| `start_date` / `end_date` | `DATE` |
| `status` | `ENUM` |

---

### `habits`
Defines recurring habits tied to a user (e.g., "drink water", "meditate", "no sugar").

| Key Fields | Type |
|---|---|
| `habit_id` | `INT AUTO_INCREMENT` (PK) |
| `user_id` | FK → `users` |
| `habit_name` | `VARCHAR(100)` |
| `active` | `TINYINT(1)` |

---

### `habit_logs`
Daily completion records for each habit. Links to `habits` via FK.

| Key Fields | Type | Notes |
|---|---|---|
| `habit_log_id` | `INT AUTO_INCREMENT` (PK) | |
| `habit_id` | FK → `habits` | |
| `log_date` | `DATE` | |
| `completed` | `TINYINT(1)` | Boolean flag |
| `value` | `DECIMAL(6,2)` | Optional quantity (e.g., oz of water) |

---

## Normalization Notes (3NF)

All tables are designed to satisfy **Third Normal Form**:

- Every non-key attribute depends on the whole primary key (2NF)
- No non-key attribute depends on another non-key attribute (3NF)

Notable design decisions that enforce normalization:

- Food nutritional data is stored once in `food` and referenced by `meal_items.food_id` no repeated macro data per meal
- Exercise metadata (category, muscle group) is stored once in `exercises` and referenced by `workout_sessions` not repeated per session
- User profile data is centralized in `users` no address or biometric data duplicated across tables

---

## Datatype Coverage

| Requirement | Table / Column |
|---|---|
| `DATE` / `DATETIME` | `users.date_of_birth`, `workout_sessions.session_datetime`, `goals.start_date` |
| `DECIMAL` / `NUMERIC` | `users.height`, `food.protein`, `meal_items.servings`, `goals.target_value` |
| `ENUM` | `users.gender`, `meals.meal_type`, `goals.status` |
| `TINYINT` (Boolean) | `habits.active`, `habit_logs.completed`, `mood_entries.mood_score` |

---

## Planned Views and Procedures (for Part 2)

**Read views / procedures (with aggregation):**
- Daily nutrition summary per user totals calories, protein, carbs, fat for a given day
- Weekly mood average average mood/energy/stress scores per user per week
- Habit completion rate percentage of days a habit was completed over a date range

**Add procedures:**
- `addWorkoutSession` inserts a new session for a user and exercise
- `addMealItem` adds a food item to an existing meal
- `addHabitLog` logs daily habit completion

**Update procedures (with cascade):**
- `updateGoalStatus` updates a goal's status (e.g., active → completed)
- `updateUserWeight` updates a user's current weight

---

## File Structure (Planned)

```
Clarke_FinalProject/
├── Part1/
│   ├── Clarke_FinalProject_ERD.pdf    # ER diagram
│   └── README.md                      # This file
├── Part2/
│   └── Clarke_FinalProject.sql        # Full database script
└── Part3/
    ├── app.py                         # Flask view layer
    ├── bll.py                         # Business logic layer
    ├── dal.py                         # Data access layer
    ├── config.ini                     # DB credentials (not committed)
    └── templates/                     # HTML templates
```