"""
Author: Shaun Clarke
Class: CSC6302 Database Principles
Module 08: Final Oroject
"""

import mysql.connector
from typing import List, Tuple
from datetime import datetime



# This class manages the database connection
class ManageDbConnection:
    def __init__(self, host: str, user: str, port: int, database: str, password: str):
        self._host = host
        self._user = user
        self._port = port
        self._database = database
        self._password = password
        self._db_object = None
        self._cursor = None
        self._is_connected: bool = False
        self._has_cursor: bool = False

    # This method connects to the database
    def connect_to_db(self):
        """
        - This method conects to the specified DB.
        """

        try:
            # Logic to only connect to the DB if it is not connected.
            if not self._is_connected:
                # Establishing DB connection with params
                self._db_object = mysql.connector.connect(
                    host=self._host,
                    user=self._user,
                    port=self._port,
                    database=self._database,
                    password=self._password
                )

                # Creating Cursor
                self._cursor = self._db_object.cursor()
                # Setting cursor and connection status
                self._has_cursor = True
                self._is_connected = True

        except mysql.connector.Error:
            # Updating cursor and connection status
            self._has_cursor = False
            self._is_connected = False
            raise

    # This method gets the DB connection
    def get_connection(self) -> object:
        if not self._is_connected or self._db_object is None:
            raise mysql.connector.Error(
                f"Database is not connected. Connect DB first.")
        return self._db_object

    # This method gets the cursor
    def get_cursor(self) -> object:
        if not self._has_cursor or self._cursor is None:
            raise mysql.connector.Error(
                f"Cursor doesn't exist. Make sure DB is connected and cursor was created.")
        return self._cursor

    # This method gets cursor status
    def get_cursor_status(self):
        return self._has_cursor

    # This method gets connections status
    def get_connection_status(self):
        return self._is_connected

    # This method closes the cursor
    def close_cursor(self):
        """
        - This method closes the cursor.
        - returns nothing.
        """
        if self._cursor is not None:
            self._cursor.close()
            # Setting cursor object to None to cleanup cursor connection
            self._cursor = None
            # Updating cursor status
            self._has_cursor: bool = False

    # This method closes the db connection
    def close_db_connection(self):
        """
        - This method closes the DB connection.
        - returns nothing.
        """
        # if the DB object is present close it
        if self._db_object is not None:
            self._db_object.close()
            # Setting database object to None to cleanup closed connection
            self._db_object = None
            # Updating DB connection status
            self._is_connected: bool = False


# This class manages the database crud actions
class DatabaseActions:
    def __init__(self, connection: ManageDbConnection):
        if not connection.get_connection_status():
            raise mysql.connector.Error(
                "DatabaseActions requires an active connection")
        self._db: object = connection.get_connection()  # Getting the DB object
        self._cursor: object = connection.get_cursor()  # Creating cursor object

    # This method performs a select query
    def select_query(self, query: str, params: tuple | None = None) -> Tuple[list[tuple], List[str]]:
        """
        - This method runs select queries(Select, functions, views etc).
        - Returns raw data, rows and column names.
        """
        # Executing query
        self._cursor.execute(query, params)
        # Getting rows and column headers from output
        column_names: List = self._cursor.column_names
        rows: List = self._cursor.fetchall()

        return rows, column_names

    # This method handles procedure calls
    def procedure_calls(self, proc_name: str, params: Tuple | None = None) -> Tuple[list[tuple], List[str]]:
        """

        - Returns raw data, rows and column names.
        """
        self._cursor.callproc(proc_name, params)

        # Lists for rows and columns data
        rows = []
        column_names = []

        # parsing output to get rows and columns headers
        for results in self._cursor.stored_results():
            column_names: List = results.column_names
            rows: List = results.fetchall()
        return rows, column_names

    def commit(self):
        self._db.commit()
        

# This class handles the database interactions for user charts in their dashboard.
class UserChartsDal:
    def __init__(self, database_action_object: DatabaseActions):
        self._db_actions = database_action_object

    # This method returns data from the dailyMoodTrends view
    def user_today_items_display(self, logged_in_user: str) -> Tuple[list[tuple], List[str]]:
        """
        Returns today's meal items for the logged in user for the Today's Items table.

        """
        params = (logged_in_user,)

        query = """
            SELECT
                `date` AS meal_datetime,
                food_name,
                servings,
                total_calories
            FROM caloriesPerDaySummaries
            WHERE username = %s
              AND `date` = CURDATE()
            ORDER BY meal_id ASC, food_name ASC
        """
        query_output = self._db_actions.select_query(query, params)
        return query_output
    
    # This method returns data from the workoutsummariees view
    def user_workout_saummarry(self, logged_in_user) -> Tuple[list[tuple], List[str]]:
        """
        Docstring for workout_saummarry_view
        
        :param self: Description
        :return: raw data, rows and column names
        :rtype: Tuple[list[tuple], List[str]]
        """
        # Query params
        params = (logged_in_user,)
        # Query
        query = "SELECT * FROM workoutSummaries WHERE username = %s"
        # getting logged in user details 
        query_output = self._db_actions.select_query(query, params)
        return query_output
    
        # # Getting all rows from the workoutsummaries view
        # query_output = self._db_actions.select_query("SELECT * FROM workoutSummaries")
        # return query_output
    
    # This method returns data from the dailyMoodTrends view
    def user_daily_mood_trends(self, logged_in_user) -> Tuple[list[tuple], List[str]]:
        """
        Docstring for daily_mood_trends_view
        
        :param self: Description
        :return: raw data, rows and column names
        :rtype: Tuple[list[tuple], List[str]]
        """
        # Query params
        params = (logged_in_user,)
        # Query
        query = "SELECT * FROM dailyMoodTrends WHERE username = %s"
        # getting logged in user details 
        query_output = self._db_actions.select_query(query, params)
        return query_output
    
        # # Getting all rows from the dailyMoodTrends view
        # query_output = self._db_actions.select_query("SELECT * FROM dailyMoodTrends")
        # return query_output
    
    # This method returns data from the caloriesPerDaySummaries view
    def user_calories_perday_saummary(self, logged_in_user) -> Tuple[list[tuple], List[str]]:
        """
        Docstring for calories_perday_saummary_view
        
        :param self: Description
        :return: raw data, rows and column names
        :rtype: Tuple[list[tuple], List[str]]
        """
        # Query params
        params = (logged_in_user,)
        # Query
        query = "SELECT * FROM caloriesPerDaySummaries WHERE username = %s"
        # getting logged in user details 
        query_output = self._db_actions.select_query(query, params)
        return query_output
    
        # # Getting all rows from the caloriesPerDaySummaries view
        # query_output = self._db_actions.select_query("SELECT * FROM caloriesPerDaySummaries")
        # return query_output
    
    # This method returns data from the dailyWeightSummary view
    def user_daily_weight_summary(self, logged_in_user) -> Tuple[list[tuple], List[str]]:
        """
        Docstring for daily_weight_summary_view
        
        :param self: Description
        :return: raw data, rows and column names
        :rtype: Tuple[list[tuple], List[str]]
        """
        
        # Query params
        params = (logged_in_user,)
        # Query
        query = "SELECT * FROM dailyWeightSummary WHERE username = %s"
        # getting logged in user details 
        query_output = self._db_actions.select_query(query, params)
        return query_output
    
        # # Getting all rows from the dailyWeightSummary view
        # query_output = self._db_actions.select_query("SELECT * FROM dailyWeightSummary")
        # return query_output
    


# This class handles interaction with the exercise table
class ExerciseDal:
    def __init__(self, database_action_object: DatabaseActions):
        self._db_actions = database_action_object

    # This method returns all rows from exercise table
    def get_all_rows(self) -> Tuple[list[tuple], List[str]]:
        """
        Docstring for get_all_rows
        
        :param self: Description
        :return: raw data, rows and column names.
        :rtype: Tuple[list[tuple], List[str]]
        """
        # getting all rows from the exercises table
        query_output = self._db_actions.select_query("SELECT * FROM exercises")
        return query_output
    

# This class handles interaction with the food table
class FoodDal:
    def __init__(self, database_action_object: DatabaseActions):
        self._db_actions = database_action_object

    # This method returns all rows from food table
    def get_all_rows(self) -> Tuple[list[tuple], List[str]]:
        """
        Docstring for get_all_rows
        
        :param self: Description
        :return: raw data, rows and column names.
        :rtype: Tuple[list[tuple], List[str]]
        """
        # getting all rows from the exercises table
        query_output = self._db_actions.select_query("SELECT * FROM food")
        return query_output

    

# This class handles interaction with the vessels table
class MealItemsDal:
    def __init__(self, database_action_object: DatabaseActions):
        self._db_actions = database_action_object

    def get_today_items_for_user(self, username: str, day: datetime.date) -> Tuple[list[tuple], List[str]]:
        """
        Returns ALL meal items for the given user for a specific date.
        Used by Log Meal Today's Items table.
        """
        query = """
            SELECT
                f.food_name,
                mi.servings,
                f.calories_per_serving,
                ROUND(mi.servings * f.calories_per_serving, 2) AS total_calories
            FROM meal_items mi
            INNER JOIN meals m ON m.meal_id = mi.meal_id
            INNER JOIN users u ON u.user_id = m.user_id
            INNER JOIN food f ON f.food_id = mi.food_id
            WHERE u.username = %s
            AND DATE(m.meal_datetime) = %s
            ORDER BY m.meal_datetime DESC, mi.meal_item_id DESC
        """
        params = (username, day)
        return self._db_actions.select_query(query, params)
    

    def get_items_for_meal(self, username: str, meal_id: int) -> Tuple[list[tuple], List[str]]:
        """
        Returns meal items for a specific meal and user.
        """
        query = """
            SELECT
                mi.meal_item_id,
                mi.meal_id,
                f.food_name,
                mi.servings,
                f.calories_per_serving,
                ROUND(mi.servings * f.calories_per_serving, 2) AS total_calories
            FROM meal_items mi
            INNER JOIN meals m ON m.meal_id = mi.meal_id
            INNER JOIN users u ON u.user_id = m.user_id
            INNER JOIN food f ON f.food_id = mi.food_id
            WHERE u.username = %s
              AND mi.meal_id = %s
            ORDER BY mi.meal_item_id ASC
        """
        params = (username, meal_id)
        query_output = self._db_actions.select_query(query, params)
        return query_output

    def get_all_meal_items_display(self) -> Tuple[list[tuple], List[str]]:
        """
        Returns all meal items with additonal needed display fields.
        """
        query = """
            SELECT
                mi.meal_item_id,
                mi.meal_id,
                u.username,
                m.meal_datetime,
                f.food_name,
                mi.servings,
                f.calories_per_serving,
                ROUND(mi.servings * f.calories_per_serving, 2) AS total_calories
            FROM meal_items mi
            INNER JOIN meals m ON m.meal_id = mi.meal_id
            INNER JOIN users u ON u.user_id = m.user_id
            INNER JOIN food f ON f.food_id = mi.food_id
            ORDER BY m.meal_datetime DESC, mi.meal_item_id DESC
        """
        query_output = self._db_actions.select_query(query)
        return query_output

    # This method returns all rows from meal_items table
    def get_all_rows(self) -> Tuple[list[tuple], List[str]]:
        """
        Docstring for get_all_rows
        
        :param self: Description
        :return: raw data, rows and column names.
        :rtype: Tuple[list[tuple], List[str]]
        """
        # getting all rows from the meal_items table
        query_output = self._db_actions.select_query("SELECT * FROM meal_items")
        return query_output


    # This method adds items to meal items table
    def add_meal_item_proc(self, meal_id: int,  food_name: str, servings: int) -> Tuple[List[Tuple], List[str]]:
        """
        Docstring for add_meal_item_proc procedure
        
        :param self: Description
        :param meal_id: Description
        :type meal_id: int
        :param food_name: Description
        :type food_name: str
        :param servings: Description
        :type servings: int
        :return: Description
        :rtype: Tuple[List[Tuple], List[str]]
        """

        proc_params = (meal_id, food_name, servings)
        # calling the addmealitems procedure
        rows, column_names = self._db_actions.procedure_calls(
            "addMealItem", proc_params)
        # Commiting chnages to DB
        self._db_actions.commit()
        return rows, column_names


# This class handles interaction with the meals table
class MealsDal:
    def __init__(self, database_action_object: DatabaseActions):
        self._db_actions = database_action_object

    def get_meal_by_id_for_user(self, username: str, meal_id: int) -> Tuple[list[tuple], List[str]]:
        """
        Returns a single meal row for a given username, meal_id.
        This way only specific user can  access their own meals.
        """
        params = (username, meal_id)

        query = """
            SELECT
                m.meal_id,
                u.username,
                m.meal_datetime,
                m.meal_type,
                m.notes
            FROM meals m
            INNER JOIN users u ON u.user_id = m.user_id
            WHERE u.username = %s
              AND m.meal_id = %s
            LIMIT 1
        """

        query_output = self._db_actions.select_query(query, params)
        return query_output

    # This method returns all rows from meals table
    def get_all_rows(self) -> Tuple[list[tuple], List[str]]:
        """
        Docstring for get_all_rows
        
        :param self: Description
        :return: raw data, rows and column names.
        :rtype: Tuple[list[tuple], List[str]]
        """
        # getting all rows from the meals table
        query_output = self._db_actions.select_query("SELECT * FROM meals")
        return query_output


    # This method adds a meal to the meals table
    def add_meal_proc(self, username: str, meal_date_time: str, meal_type: str, notes: str, meal_id_output=None) -> Tuple[List[Tuple], List[str]]:
        """
        Docstring for add_meal_proc
        
        :param self: Description
        :param username: Description
        :type username: str
        :param meal_date_time: Description
        :type meal_date_time: str
        :param meal_type: Description
        :type meal_type: str
        :param notes: Description
        :type notes: str
        :param meal_id_output: Description
        :return: Description
        :rtype: Tuple[List[Tuple], List[str]]
        """
        proc_params = (username, meal_date_time, meal_type, notes, meal_id_output)
        # calling the add meal procedure
        rows, column_names = self._db_actions.procedure_calls(
            "addMeal", proc_params)
        # Commiting chnages to DB
        self._db_actions.commit()
        return rows, column_names
    

# This class handles interaction with the mood_entries table
class MoodEntriesDal:
    def __init__(self, database_action_object: DatabaseActions):
        self._db_actions = database_action_object

    # This method returns all rows from mood_entries table
    def get_all_rows(self) -> Tuple[list[tuple], List[str]]:
        """
        Docstring for get_all_rows
        
        :param self: Description
        :return: raw data, rows and column names.
        :rtype: Tuple[list[tuple], List[str]]
        """
        # getting all rows from the mood_entries table
        query_output = self._db_actions.select_query("SELECT * FROM mood_entries")
        return query_output

    # This method adds a mmod log to the logMood table
    def log_mood_proc(self, username: str, date_time: str, mood_score: int, energy_level: int, stress_level: int, note: str) -> Tuple[List[Tuple], List[str]]:
        """
        Docstring for add_vessel_proc
        
        :param self: Description
        :param username: Description
        :type username: str
        :param date_time: Description
        :type date_time: str
        :param mood_score: Description
        :type mood_score: int
        :param energy_level: Description
        :type energy_level: int
        :param stress_level: Description
        :type stress_level: int
        :param note: Description
        :type note: str
        :return: Description
        :rtype: Tuple[List[Tuple], List[str]]
        """
        proc_params = (username, date_time, mood_score, energy_level, stress_level, note)
        # calling the add logMood procedure
        rows, column_names = self._db_actions.procedure_calls(
            "logMood", proc_params)
        # Commiting chnages to DB
        self._db_actions.commit()
        return rows, column_names


# This class handles interaction with the users table
class UsersDal:
    def __init__(self, database_action_object: DatabaseActions):
        self._db_actions = database_action_object


    # This method returns all rows from users table
    def get_all_rows(self) -> Tuple[list[tuple], List[str]]:
        """
        Docstring for get_all_rows
        
        :param self: Description
        :return: raw data, rows and column names.
        :rtype: Tuple[list[tuple], List[str]]
        """
        # getting logged in user details from the users table
        query_output = self._db_actions.select_query(f"SELECT * FROM users")
        return query_output
    
    # This method returns all rows for a specific user from users table
    def get_user_details(self, logged_in_user) -> Tuple[list[tuple], List[str]]:
        """
        Docstring for get_all_rows
        
        :param self: Description
        :return: raw data, rows and column names.
        :rtype: Tuple[list[tuple], List[str]]
        """
        # Query params
        params = (logged_in_user,)
        # Query
        query = "SELECT first_name, last_name, email, username, date_of_birth, gender, height, weight FROM users WHERE username = %s"
        # getting logged in user details from the users table
        query_output = self._db_actions.select_query(query, params)
        return query_output
    
    # This method validates username and password for specific user from users table
    def validate_user_creds(self, username: str, password: str) -> Tuple[list[tuple], List[str]]:
        """
        Docstring for validate_user_creds

        -1 user not found
        -2 password not found
        0 user account exists
        
        :param self: Description
        :param username: Description
        :type username: str
        :param password: Description
        :type password: str
        :return: Description
        :rtype: Tuple[list[tuple], List[str]]
        """
        # Query params
        params = (username, password,)
        rows, column_names = self._db_actions.procedure_calls(
            "validateUser", params)
        # Commiting chnages to DB
        self._db_actions.commit()
        return rows, column_names

    # This method adds a user to the user's table
    def create_user_proc(self, first_name: str, last_name: str, email: str, password: str, username: str, dob: str, gender: str, height: int, weight: int) -> Tuple[List[Tuple], List[str]]:

        # Geting the current date and time
        now = datetime.now()

        # Formatting the datetime object into the desired string format that the created at column expects
        created_at_date = now.strftime("%Y-%m-%d %H:%M:%S")
        
        proc_params = (first_name, last_name, email, password, created_at_date, username, dob, gender, height, weight)
        # calling the createUser procedure
        rows, column_names = self._db_actions.procedure_calls(
            "createUser", proc_params)
        # Commiting chnages to DB
        self._db_actions.commit()
        return rows, column_names

    # This method delete's a user account
    def delete_account_proc(self, username: str) -> Tuple[List[Tuple], List[str]]:
        
        proc_params = (username,)
        # calling the deleteAccount procedure
        rows, column_names = self._db_actions.procedure_calls(
            "deleteAccount", proc_params)
        # Commiting chnages to DB
        self._db_actions.commit()
        return rows, column_names
    

    # This method allows a user to reset their password
    def reset_password_proc(self, email: str, password: str, username: str) -> Tuple[List[Tuple], List[str]]:
        
        proc_params = (password, username,email)
        # calling the resetPassword procedure
        rows, column_names = self._db_actions.procedure_calls(
            "resetPassword", proc_params)
        # Commiting chnages to DB
        self._db_actions.commit()
        return rows, column_names
    

# This class handles interaction with the weight_logs table
class WeightLogsDal:
    def __init__(self, database_action_object: DatabaseActions):
        self._db_actions = database_action_object

    # This method returns all rows from weight_logs table
    def get_all_rows(self) -> Tuple[list[tuple], List[str]]:
        """
        Docstring for get_all_rows
        
        :param self: Description
        :return: raw data, rows and column names.
        :rtype: Tuple[list[tuple], List[str]]
        """
        # getting all rows from the weight_logs table
        query_output = self._db_actions.select_query("SELECT * FROM weight_logs")
        return query_output

    # This method adds the user's weight to the weight_logs table
    def log_user_weight_proc(self, username: str, weight: int, created_at_date: str) -> Tuple[List[Tuple], List[str]]:
        """
        Docstring for log_user_weight_proc
        
        :param self: Description
        :param username: Description
        :type username: str
        :param weight: Description
        :type weight: int
        :param created_at_date: Description
        :type created_at_date: str
        :return: Description
        :rtype: Tuple[List[Tuple], List[str]]
        """
        # # Geting the current date and time
        # now = datetime.now()

        # # Formatting the datetime object into the desired string format that the created at column expects
        # created_at_date = now.strftime("%Y-%m-%d %H:%M:%S")

        proc_params = (username, weight, created_at_date)
        # calling the logWeight procedure
        rows, column_names = self._db_actions.procedure_calls(
            "logWeight", proc_params)
        # Commiting chnages to DB
        self._db_actions.commit()
        return rows, column_names
    
    # Thjis method returns recent weigh-ins for a given user 
    def get_recent_weights_display(self, username: str, limit: int = 10) -> Tuple[list[tuple], List[str]]:
        """
        Thjis method returns recent weigh-ins for a given user 
        used to populate the recent weigh-ins table
        """
        query = """
            SELECT
                wl.weight_datetime,
                wl.weight
            FROM weight_logs wl
            INNER JOIN users u ON u.user_id = wl.user_id
            WHERE u.username = %s
            ORDER BY wl.weight_datetime DESC
            LIMIT %s
        """
        params = (username, int(limit))
        return self._db_actions.select_query(query, params)

    # This method returns full weight history for a given user
    def get_weight_history_display(self, username: str) -> Tuple[list[tuple], List[str]]:
        """
        This method returns full weight history for a given user in user friendly table format
        This is used by the weight history page
        """
        query = """
            SELECT
                wl.weight_datetime,
                wl.weight
            FROM weight_logs wl
            INNER JOIN users u ON u.user_id = wl.user_id
            WHERE u.username = %s
            ORDER BY wl.weight_datetime DESC
        """
        params = (username,)
        return self._db_actions.select_query(query, params)


# This class handles interaction with the workout_sessions table
class WorkoutSessionsDal:
    def __init__(self, database_action_object: DatabaseActions):
        self._db_actions = database_action_object

    def get_workout_history_display(self, username: str) -> Tuple[list[tuple], List[str]]:
        """
        Returns ALL workout sessions for a user with user friendly column names.
        Used by workout history page.
        """
        query = """
            SELECT
                ws.session_id,
                DATE(ws.session_datetime) AS session_date,
                e.exercise_name AS workout_name,
                ws.duration_minutes,
                ws.notes
            FROM workout_sessions ws
            INNER JOIN users u ON u.user_id = ws.user_id
            INNER JOIN exercises e ON e.exercise_id = ws.exercise_id
            WHERE u.username = %s
            ORDER BY ws.session_datetime DESC, ws.session_id DESC
        """
        params = (username,)
        return self._db_actions.select_query(query, params)
    

    def get_recent_workouts_display(self, username: str, limit: int = 10) -> Tuple[list[tuple], List[str]]:
        """
        Returns recent workouts for a user.
        Used by the recent workouts table
        """
        query = """
            SELECT
                ws.session_id,
                ws.session_datetime,
                e.exercise_name,
                ws.duration_minutes,
                ws.sets,
                ws.reps,
                ws.weight,
                ws.notes
            FROM workout_sessions ws
            INNER JOIN users u ON u.user_id = ws.user_id
            INNER JOIN exercises e ON e.exercise_id = ws.exercise_id
            WHERE u.username = %s
            ORDER BY ws.session_datetime DESC, ws.session_id DESC
            LIMIT %s
        """
        params = (username, limit)
        return self._db_actions.select_query(query, params)

    # This method returns all rows from workout_sessions table
    def get_all_rows(self) -> Tuple[list[tuple], List[str]]:
        """
        Docstring for get_all_rows
        
        :param self: Description
        :return: raw data, rows and column names.
        :rtype: Tuple[list[tuple], List[str]]
        """
        # getting all rows from the workout_sessions table
        query_output = self._db_actions.select_query("SELECT * FROM workout_sessions")
        return query_output

    # This method adds the user's workouts to the workout_sessions table
    def log_user_workout_proc(
            self, username: str, exercise: str, date_time: str,
            duration_in_minutes: int, notes: str, sets: int, reps: int, weight: int) -> Tuple[List[Tuple], List[str]]:
        """
        Docstring for log_user_workout_proc
        
        :param self: Description
        :param username: Description
        :type username: str
        :param exercise: Description
        :type exercise: str
        :param date_time: Description
        :type date_time: str
        :param duration_in_minutes: Description
        :type duration_in_minutes: int
        :param notes: Description
        :type notes: str
        :param sets: Description
        :type sets: int
        :param reps: Description
        :type reps: int
        :param weight: Description
        :type weight: int
        :return: Description
        :rtype: Tuple[List[Tuple], List[str]]
        """
        proc_params = (username, exercise, date_time, duration_in_minutes, notes, sets, reps, weight)
        # calling the logWorkout procedure
        rows, column_names = self._db_actions.procedure_calls(
            "logWorkout", proc_params)
        # Commiting chnages to DB
        self._db_actions.commit()
        return rows, column_names
