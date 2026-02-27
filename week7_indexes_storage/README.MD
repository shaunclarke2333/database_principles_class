# Health & Wellness Tracker Final Project Part 2: Database

**Course:** CSC6302 Database Principles  
**Final Project Part 2 (Database Creation)**  
**Author:** Shaun Clarke

---

## Project Overview

This is the database layer for the **Mind Body Dashboard (MBD)** a personal health and wellness tracking application. The database stores user profiles, workout sessions, nutrition logs, mood entries, and weight history. All data is fully normalized to 3NF, and the schema is supported by views, scalar functions, and stored procedures covering read, add, update, and delete operations.

---

## Database: `mbd`

The script drops and recreates the `mbd` database each run, making it fully idempotent.

---

## Schema Overview

The database contains **7 tables**:

### `users`
Central table. Stores account credentials and biometric profile data.

| Column | Type | Notes |
|---|---|---|
| `user_id` | `INT AUTO_INCREMENT` | Primary key |
| `email` | `VARCHAR(150) UNIQUE` | Must be unique |
| `username` | `VARCHAR(100) UNIQUE` | Must be unique |
| `date_of_birth` | `DATE` | |
| `gender` | `ENUM('male','female','nonbinary','other')` | |
| `height` / `weight` | `DECIMAL(5,2)` | In cm / kg |
| `password_hash` | `VARCHAR(255)` | Hashed credential |

---

### `exercises`
Reference table for exercise types. No FK looked up by workout sessions.

| Column | Type |
|---|---|
| `exercise_id` | `INT AUTO_INCREMENT` (PK) |
| `exercise_name` | `VARCHAR(100)` |
| `exercise_category` | `VARCHAR(50)` |
| `muscle_group` | `VARCHAR(50)` |

---

### `workout_sessions`
Logs individual exercise sessions per user.

| Column | Type | Notes |
|---|---|---|
| `session_id` | `INT AUTO_INCREMENT` | PK |
| `user_id` | `INT` | FK → `users` (CASCADE) |
| `exercise_id` | `INT` | FK → `exercises` (CASCADE) |
| `session_datetime` | `DATETIME` | |
| `duration_minutes` | `INT` | |
| `sets` / `reps` | `INT NULL` | Optional for cardio |
| `weight` | `DECIMAL(6,2) NULL` | In kg |

---

### `meals`
Logs meal events per user.

| Column | Type | Notes |
|---|---|---|
| `meal_id` | `INT AUTO_INCREMENT` | PK |
| `user_id` | `INT` | FK → `users` (CASCADE) |
| `meal_datetime` | `DATETIME` | |
| `meal_type` | `ENUM('breakfast','lunch','dinner','snack')` | |

---

### `food`
Reference table of food items with nutritional data per serving.

| Column | Type |
|---|---|
| `food_id` | `INT AUTO_INCREMENT` (PK) |
| `food_name` | `VARCHAR(100)` |
| `calories_per_serving` | `INT` |
| `protein` / `carbs` / `fat` | `DECIMAL(6,2)` |

---

### `meal_items`
Junction table linking meals to food items. Stores quantity (servings).  
Total macros are computed at query time by multiplying `servings × per-serving values`.

| Column | Type | Notes |
|---|---|---|
| `meal_item_id` | `INT AUTO_INCREMENT` | PK |
| `meal_id` | `INT` | FK → `meals` (CASCADE) |
| `food_id` | `INT` | FK → `food` (CASCADE) |
| `servings` | `DECIMAL(5,2)` | Scales all macro calculations |

---

### `mood_entries`
Daily mood, energy, and stress logs per user with optional free-text notes.

| Column | Type |
|---|---|
| `mood_id` | `INT AUTO_INCREMENT` (PK) |
| `user_id` | `INT` FK → `users` (CASCADE) |
| `entry_datetime` | `DATETIME` |
| `mood_score` / `energy_level` / `stress_level` | `TINYINT` |

---

### `weight_logs`
Timestamped weight entries per user for tracking trends over time.

| Column | Type |
|---|---|
| `weight_id` | `INT AUTO_INCREMENT` (PK) |
| `user_id` | `INT` FK → `users` (CASCADE) |
| `weight` | `DECIMAL(5,2)` |
| `weight_datetime` | `DATETIME` |

---

## Datatype Coverage

| Requirement | Table / Column |
|---|---|
| `DATETIME` / `DATE` | `workout_sessions.session_datetime`, `users.date_of_birth`, `weight_logs.weight_datetime` |
| `DECIMAL` / `NUMERIC` | `food.protein`, `meal_items.servings`, `users.height`, `workout_sessions.weight` |
| `ENUM` | `users.gender`, `meals.meal_type` |
| `TINYINT` (Boolean/Score) | `mood_entries.mood_score`, `mood_entries.energy_level`, `mood_entries.stress_level` |

---

## Normalization (3NF)

All tables satisfy Third Normal Form:

- Every non-key attribute depends on the whole primary key, not a subset
- No transitive dependencies between non-key attributes

Key design decisions enforcing this:

- Nutritional data lives once in `food` and is scaled at query time via `meal_items.servings` macros are never stored redundantly per meal
- Exercise metadata (category, muscle group) lives once in `exercises` and is referenced by `workout_sessions`
- All user-specific data (profile, logs) is tied back to `users.user_id` via FK no user data is duplicated across tables

---

## Views

### `dailyMoodTrends`
Aggregates mood entries by user and day. Returns average mood score and stress level per day. Feeds the mood trend chart in the application.

```sql
SELECT * FROM dailyMoodTrends;
```

### `workoutSummaries`
Aggregates workout sessions by user and day. Returns session count and total duration per day. Feeds the workout consistency chart.

```sql
SELECT * FROM workoutSummaries;
```

### `caloriesPerDaySummaries`
Joins `meal_items`, `meals`, and `food` to compute total calories, protein, carbs, and fat per meal per user per day. Macro totals are computed as `SUM(servings × per_serving_value)`. Feeds the macro chart.

```sql
SELECT * FROM caloriesPerDaySummaries;
```

### `dailyWeightSummary`
Returns each user's weight log entries grouped by date. Feeds the weight trend chart.

```sql
SELECT * FROM dailyWeightSummary;
```

---

## Functions

| Function | Parameters | Returns | Notes |
|---|---|---|---|
| `getUserID` | `username` | `INT` | Returns `-1` if not found |
| `getUserName` | `username` | `VARCHAR` | Returns `-1` if not found |
| `getUserEmail` | `email` | `VARCHAR` | Returns `-1` if not found |
| `getExerciseID` | `exercise_name` | `INT` | Returns `-1` if not found |
| `getFoodID` | `food_name` | `INT` | Returns `-1` if not found |

---

## Stored Procedures

### Add Operations

**`createUser`** — Creates a new user account. Returns `-1` if username already exists, `-2` if email already exists, or the new `user_id` on success.

```sql
CALL createUser('Jane', 'Doe', 'jane@example.com', 'hash_abc', NOW(), 'JaneD', '1992-05-10', 'female', 165.00, 62.00);
```

**`logMood`** — Logs a mood entry for an existing user by username. Returns `-2` if user not found, `0` on success.

```sql
CALL logMood('ShaunC', '2025-10-13 07:00:00', 8, 7, 3, 'Feeling great today');
```

**`logWorkout`** Logs a workout session by username and exercise name. Returns `-3` if both not found, `-2` if user not found, `-1` if exercise not found, `0` on success.

```sql
CALL logWorkout('ShaunC', 'Back Squat', '2025-10-13 06:00:00', 45, 'Strong session', 4, 5, 82.50);
```

**`addMeal`** Creates a new meal record for a user. Returns the new `meal_id` via an `OUT` parameter.

```sql
SET @meal_id = NULL;
CALL addMeal('ShaunC', '2025-10-16 07:30:00', 'breakfast', 'Oats and berries', @meal_id);
SELECT @meal_id;
```

**`addMealItem`** Adds a food item to an existing meal by meal ID and food name. Returns `-3` if both not found, `-2` if meal ID is null, `-1` if food not found, `0` on success.

```sql
CALL addMealItem(@meal_id, 'Overnight Oats Base', 1.00);
```

**`logWeight`** Logs a timestamped weight entry for a user. Returns `-1` if user not found, `0` on success.

```sql
CALL logWeight('ShaunC', 106.50, '2025-10-13 07:00:00');
```

---

### Update Operations

**`resetPassword`** Updates a user's password hash. Validates that the provided username and email match the same record before updating. Returns `-3` if they don't match, `0` on success. Changes propagate via FK cascades.

```sql
CALL resetPassword('new_hash_value', 'ShaunC', 'shaun@example.com');
```

---

### Delete Operations

**`deleteAccount`** Deletes a user by username. All related records in `mood_entries`, `workout_sessions`, `meals`, `meal_items`, and `weight_logs` are removed automatically via `ON DELETE CASCADE`. Returns `-1` if user not found, `0` on success.

```sql
CALL deleteAccount('ShaunC');
```

---

## Data Summary

| Table | Rows |
|---|---|
| `users` | 10 |
| `exercises` | 10 |
| `meals` | 10 |
| `food` | 11 |
| `meal_items` | 20 |
| `mood_entries` | **30** |
| `workout_sessions` | 12 |
| `weight_logs` | 24 |

`mood_entries` is the largest table with 30 rows, satisfying the minimum requirement.

---

## Prerequisites

- MySQL 8.0+
- MySQL Workbench or the MySQL command-line client

---

## How to Run

### Option 1: MySQL Command Line

```bash
mysql -u your_username -p < Clarke_FinalProject_Part2.sql
```

### Option 2: MySQL Workbench

1. Open MySQL Workbench and connect to your local MySQL server.
2. Go to **File > Open SQL Script** and select `Clarke_FinalProject_Part2.sql`.
3. Click the **Execute** (lightning bolt) button.

### Option 3: Source Command

```sql
SOURCE /path/to/Clarke_FinalProject_Part2.sql;
```

> The script drops and recreates the `mbd` database each run it is fully idempotent.

---

## File Structure

```
Clarke_FinalProject/
├── Part1/
│   ├── Clarke_FinalProject_ERD.pdf
│   └── README.md
├── Part2/
│   ├── Clarke_FinalProject_Part2.sql    # This script
│   └── README.md                        # This file
└── Part3/
    └── (application layer — see Part 3 README)
```