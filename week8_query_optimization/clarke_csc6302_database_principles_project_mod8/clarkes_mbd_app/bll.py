"""
Author: Shaun Clarke
Class: CSC6302 Database Principles
Module 08: Final Oroject
"""

from typing import List, Tuple, Optional
import dal
from datetime import datetime


# This class manages UserCHartsDal interactions
class UserChartsService:
    def __init__(self, user_charts_table_actions: dal.UserChartsDal):
        self.user_charts_table_actions = user_charts_table_actions

    # This method gets today's meal items for the logged-in user
    def get_user_today_items_display(self, logged_in_user: str) -> Tuple[List[Tuple], List[str]]:
        """
        Returns today's meal items for display in the Today's Items table.

        """
        rows, column_names = self.user_charts_table_actions.user_today_items_display(
            logged_in_user
        )
        return rows, column_names

    # This method gets the workout_saummarry from the workout_saummarry view
    def get_user_workout_saummary(self, logged_in_user) -> Tuple[List[Tuple], List[str]]:
        """
        Docstring for get_user_workout_saummary

        :param self: Description
        :param logged_in_user: Description
        :return: Description
        :rtype: Tuple[List[Tuple], List[str]]
        """

        rows, column_names = self.user_charts_table_actions.user_workout_saummarry(
            logged_in_user)
        return rows, column_names

        # # Getting all rows from the workout_saummarry view
        # rows, column_names = self.user_charts_table_actions.workout_saummarry()
        # return rows, column_names

    # This method gets the daily_mood_trends from the daily_mood_trends view
    def get_user_daily_mood_trends(self, logged_in_user) -> Tuple[List[Tuple], List[str]]:
        """
        Docstring for get_daily_mood_trends

        :param self: Description
        :return: Description
        :rtype: Tuple[List[Tuple], List[str]]
        """
        # Getting all rows from the daily_mood_trends view
        rows, column_names = self.user_charts_table_actions.user_daily_mood_trends(
            logged_in_user)
        return rows, column_names

    # This method gets the calories_perday_saummary from the calories_perday_saummary view
    def get_user_calories_perday_saummary(self, logged_in_user) -> Tuple[List[Tuple], List[str]]:
        """
        Docstring for get_calories_perday_saummary

        :param self: Description
        :return: Description
        :rtype: Tuple[List[Tuple], List[str]]
        """
        # Getting all rows from the calories_perday_saummaryview
        rows, column_names = self.user_charts_table_actions.user_calories_perday_saummary(
            logged_in_user)
        return rows, column_names

    # This method gets the daily_weight_summary from the daily_weight_summary view
    def get_user_daily_weight_summary(self, logged_in_user) -> Tuple[List[Tuple], List[str]]:
        """
        Docstring for get_daily_weight_summary

        :param self: Description
        :return: Description
        :rtype: Tuple[List[Tuple], List[str]]
        """
        # Getting all rows from the daily_weight_summary view
        rows, column_names = self.user_charts_table_actions.user_daily_weight_summary(
            logged_in_user)
        return rows, column_names


# This class manages ExerciseDal interactions
class ExerciseService:
    def __init__(self, exercise_table_actions: dal.ExerciseDal):
        self.exercise_table_actions = exercise_table_actions

    # This method gets all the exercises from the exercise db table
    def get_all_exercises(self) -> Tuple[List[Tuple], List[str]]:
        """
        Docstring for get_all_exercises

        :param self: Description
        :return: Description
        :rtype: Tuple[List[Tuple], List[str]]
        """
        # Getting all rows from exercise table
        rows, column_names = self.exercise_table_actions.get_all_rows()
        return rows, column_names


# This class manages FoodDal interactions
class FoodService:
    def __init__(self, food_table_actions: dal.FoodDal):
        self.food_table_actions = food_table_actions

    # This method gets all the food from the food db table
    def get_all_foods(self) -> Tuple[List[Tuple], List[str]]:
        """
        Docstring for get_all_foods

        :param self: Description
        :return: Description
        :rtype: Tuple[List[Tuple], List[str]]
        """
        # Getting all rows from food table
        rows, column_names = self.food_table_actions.get_all_rows()
        return rows, column_names


# This class manages MealItemsDal interactions
class MealItemsService:
    def __init__(self, meal_items_table_actions: dal.MealItemsDal):
        self.meal_items_table_actions = meal_items_table_actions

    def get_today_items_for_user(self, username: str, day: datetime.date) -> Tuple[List[Tuple], List[str]]:
        """
        Returns all meal items logged today for the user.
        """
        if not username or not username.strip():
            raise ValueError("username cannot be empty")

        return self.meal_items_table_actions.get_today_items_for_user(username, day)


    def get_items_for_meal(self, username: str, meal_id: int) -> Tuple[List[Tuple], List[str]]:
        """
        Returns meal items for a given meal owned by the given user.
        Used by Log Meal Today's Items table.
        """
        if not username or not username.strip():
            raise ValueError("username cannot be empty")
        if meal_id is None or int(meal_id) <= 0:
            raise ValueError("meal_id must be a positive integer")

        rows, column_names = self.meal_items_table_actions.get_items_for_meal(
            username, int(meal_id)
        )
        return rows, column_names

    def get_meal_items_display(self) -> Tuple[List[Tuple], List[str]]:
        """
        Returns all meal items with joined display fields.
        """
        rows, column_names = self.meal_items_table_actions.get_all_meal_items_display()
        return rows, column_names

    # This method gets all meal_items from the meal_items db table
    def get_all_meal_items(self) -> Tuple[List[Tuple], List[str]]:
        """
        Docstring for get_all_meal_items

        :param self: Description
        :return: Description
        :rtype: Tuple[List[Tuple], List[str]]
        """
        # Getting all rows from meal_items table
        rows, column_names = self.meal_items_table_actions.get_all_rows()
        return rows, column_names

    # This method adds a meal item to the meal_items table
    def add_meal_item(self, meal_id: int,  food_name: str, servings: int) -> Tuple[List[Tuple], List[str]]:
        """
        Docstring for add_meal_item

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

        # validating inputs
        if not isinstance(servings, (int,float)):
            raise ValueError(
                f"Servings must be a number")

        # adding vessel to vessel table
        rows, column_names = self.meal_items_table_actions.add_meal_item_proc(
            meal_id, food_name, servings)
        return rows, column_names


# This class manages MealItemsDal interactions
class MealsService:
    def __init__(self, meals_table_actions: dal.MealsDal):
        self.meals_table_actions = meals_table_actions

    def get_meal_by_id(self, username: str, meal_id: int) -> Tuple[List[Tuple], List[str]]:
        """
        Gets a single meal by meal_id for the given username.

        :param username: Logged-in user's username
        :param meal_id: Meal ID to look up
        :return: rows and column names
        """
        # Basic validation (optional but good practice)
        if not username or not username.strip():
            raise ValueError("username cannot be empty")
        if meal_id is None or int(meal_id) <= 0:
            raise ValueError("meal_id must be a positive integer")

        rows, column_names = self.meals_table_actions.get_meal_by_id_for_user(username, int(meal_id))
        return rows, column_names

    # This method gets all meals from the meals db table
    def get_all_meal(self) -> Tuple[List[Tuple], List[str]]:
        """
        Docstring for get_all_meal

        :param self: Description
        :return: Description
        :rtype: Tuple[List[Tuple], List[str]]
        """
        # Getting all rows from meal_items table
        rows, column_names = self.meals_table_actions.get_all_rows()
        return rows, column_names

    # This method adds a meal item to the meal_items table
    def add_meal(
            self, username: str, meal_date_time: str, meal_type: str,
            notes: Optional[str] = None, meal_id_output: Optional[int] = None) -> Tuple[List[Tuple], List[str]]:
        """
        Docstring for add_meal

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
        :type meal_id_output: Optional[int]
        :return: Description
        :rtype: Tuple[List[Tuple], List[str]]
        """
        # Validating inputs
        # if not vessel_name or not vessel_name.strip():
        #     raise ValueError(f"Vessel name cannot be empty")

        # Adding meal to table
        rows, column_names = self.meals_table_actions.add_meal_proc(
            username, meal_date_time, meal_type, notes, meal_id_output)
        # Getting meal ID row value from list of tuple
        meal_id = rows[0][0]

        # If we found a Meal ID
        if meal_id != -1:
            return rows, column_names

        # If no Meal ID found -1 will be the row value
        return rows, column_names


# This class manages MoodEntriesDal interactions
class MoodEntriesService:
    def __init__(self, mood_entries_table_actions: dal.MoodEntriesDal):
        self.mood_entries_table_actions = mood_entries_table_actions

    # This method gets all rows from the mood_entries db table
    def get_all_mood_entries(self) -> Tuple[List[Tuple], List[str]]:
        # Getting all rows from mood_entries table
        rows, column_names = self.mood_entries_table_actions.get_all_rows()
        return rows, column_names

    # This method adds a mood entry to the mood_entries table
    def add_mood_entries(
            self, username: str, date_time: str, mood_score: int, energy_level: int,
            stress_level: int, note: Optional[int] = None) -> Tuple[List[Tuple], List[str]]:

        # validating inputs
        if not isinstance(mood_score, int) or mood_score > 10 or mood_score < 1:
            raise ValueError(
                f"Mood score must be a number from 1 - 10")
        if not isinstance(energy_level, int) or energy_level > 10 or energy_level < 1:
            raise ValueError(
                f"Energy level must be a number from 1 - 10")
        if not isinstance(stress_level, int) or stress_level > 10 or stress_level < 1:
            raise ValueError(
                f"Stress level must be a number from 1 - 10")

        # calling log mood procedure to add a mood to mood entries table
        rows, column_names = self.mood_entries_table_actions.log_mood_proc(
            username, date_time, mood_score, energy_level, stress_level, note)
        return rows, column_names


# This class manages UserDal interactions
class UserService:
    def __init__(self, users_table_actions: dal.UsersDal):
        self.users_table_actions = users_table_actions

    # This method gets a specific user's details from the users db table
    def get_a_user_creds(self, username, passwords) -> Tuple[List[Tuple], List[str]]:
        """
        Docstring for get_a_user_creds

        :param self: Description
        :param username: Description
        :param passwords: Description
        :return: Description
        :rtype: Tuple[List[Tuple], List[str]]
        """
        # Getting specific user creds from users table
        rows, column_names = self.users_table_actions.get_user_creds(
            username, passwords)
        return rows, column_names

    # This method gets all rows from the users db table
    def get_all_users(self) -> Tuple[List[Tuple], List[str]]:
        """
        Docstring for get_all_users

        :param self: Description
        :return: Description
        :rtype: Tuple[List[Tuple], List[str]]
        """
        # Getting all rows from users table
        rows, column_names = self.users_table_actions.get_all_rows()
        return rows, column_names

    # This method gets a specific user's details from the users db table
    def get_a_user_details(self, logged_in_user) -> Tuple[List[Tuple], List[str]]:
        """
        Docstring for get_a_user_details

        :param self: Description
        :param logged_in_user: Description
        :return: Description
        :rtype: Tuple[List[Tuple], List[str]]
        """
        # Getting specific user details from users table
        rows, column_names = self.users_table_actions.get_user_details(
            logged_in_user)
        return rows, column_names

    # This method validates a specific user's creds in the users db table
    def get_user_account(self, username: str, password: str) -> Tuple[List[Tuple], List[str]]:
        """
        Docstring for get_user_account
        -1 user not found
        -2 password not found
        0 user account exists

        :param self: Description
        :param username: Description
        :type username: str
        :param password: Description
        :type password: str
        :return: Description
        :rtype: Tuple[List[Tuple], List[str]]
        """
        # Getting specific user details from users table
        rows, column_names = self.users_table_actions.validate_user_creds(
            username, password)
        row_value = rows[0][0]

        if row_value == -1:
            raise Exception(f"User account not found")

        if row_value == -2:
            raise Exception(f"User password not found")

        # If account exists
        if row_value == 0:
            return rows, column_names

        return rows, column_names

    # This method adds a user to the users table
    def add_user(
            self, first_name: str, last_name: str, email: str, password: str,
            username: str, dob: str, gender: str, height: int, weight: int) -> Tuple[List[Tuple], List[str]]:
        """
        Docstring for add_user

        :param self: Description
        :param first_name: Description
        :type first_name: str
        :param last_name: Description
        :type last_name: str
        :param email: Description
        :type email: str
        :param password: Description
        :type password: str
        :param username: Description
        :type username: str
        :param dob: Description
        :type dob: str
        :param gender: Description
        :type gender: str
        :param height: Description
        :type height: int
        :param weight: Description
        :type weight: int
        :return: Description
        :rtype: Tuple[List[Tuple], List[str]]
        """

        # Removing any leading or trailing white space
        parameters_to_strip = [first_name,
                               last_name, email, password, username]
        stripped_parameters = [p.strip() for p in parameters_to_strip]

        first_name = stripped_parameters[0]
        last_name = stripped_parameters[1]
        email = stripped_parameters[2]
        password = stripped_parameters[3]
        username = stripped_parameters[4]

        # validating inputs
        if not isinstance(height, (int, float)):
            raise ValueError(
                f"Height must be a number in inches")
        if not isinstance(weight, (int, float)):
            raise ValueError(
                f"Weight must be a number")

        # calling the create user procedure procedure to add a procedure to the users table
        rows, column_names = self.users_table_actions.create_user_proc(
            first_name, last_name, email, password, username, dob, gender, height, weight)
        return rows, column_names

    # This method updates the user's password in the user's table
    def reset_user_password(self, email: str, password: str, username: str) -> Tuple[List[Tuple], List[str]]:
        """
        Docstring for reset_user_password

        :param self: Description
        :param email: Description
        :type email: str
        :param password: Description
        :type password: str
        :param username: Description
        :type username: str
        :return: Description
        :rtype: Tuple[List[Tuple], List[str]]
        """

        # Removing any leading or trailing white space
        parameters_to_strip = [email, password, username]
        stripped_parameters = [p.strip() for p in parameters_to_strip]

        email = stripped_parameters[0]
        password = stripped_parameters[1]
        username = stripped_parameters[2]

        # validating inputs
        if email is None:
            raise ValueError(
                f"Email cannot be empty")
        if password is None:
            raise ValueError(
                f"Password cannot be empty")
        if username is None:
            raise ValueError(
                f"Username cannot be empty")

        # calling the create user procedure procedure to add a procedure to the users table
        rows, column_names = self.users_table_actions.reset_password_proc(
            email, password, username)
        return rows, column_names

    # This method delete's a user from the users db table, which deletes the user's account
    def delete_user_account(self, logged_in_user) -> Tuple[List[Tuple], List[str]]:
        """
        Docstring for delete_user_account

        :param self: Description
        :param logged_in_user: Description
        :return: Description
        :rtype: Tuple[List[Tuple], List[str]]
        """
        # Getting specific user details from users table
        rows, column_names = self.users_table_actions.delete_account_proc(
            logged_in_user)
        return rows, column_names


# This class manages WeightLogsDal interactions
class WeightLogService:
    def __init__(self, weight_logs_table_actions: dal.WeightLogsDal):
        self.weight_logs_table_actions = weight_logs_table_actions

    # This method gets all rows from the weight_logs db table
    def get_all_weight_logs(self) -> Tuple[List[Tuple], List[str]]:
        # Getting all rows from weight_logs table
        rows, column_names = self.weight_logs_table_actions.get_all_rows()
        return rows, column_names

    # This method adds a user's weight to the weight_logs table
    def log_user_weight(self, username: str, weight: int, date_time: str) -> Tuple[List[Tuple], List[str]]:

        # validating inputs
        if username is None:
            raise ValueError(
                f"Username cannot be empty")

        if not isinstance(weight, (int, float)):
            raise ValueError(
                f"Weight must be a number")

        # calling log user weight procedure to add a users's weight to the weight table
        rows, column_names = self.weight_logs_table_actions.log_user_weight_proc(
            username, weight, date_time)
        return rows, column_names
    
    # This method populates the recent weigh-ins for the right side table on weight_log.html
    def get_recent_weights_display(self, username: str, limit: int = 10) -> Tuple[List[Tuple], List[str]]:
        """
        Docstring for get_recent_weights_display
        This method populates the recent weigh-ins for the right-side table on weight_log.html
        
        :param self: Description
        :param username: Description
        :type username: str
        :param limit: Description
        :type limit: int
        :return: Description
        :rtype: Tuple[List[Tuple], List[str]]
        """
        if not username or not username.strip():
            raise ValueError("username cannot be empty")
        if limit is None or int(limit) <= 0:
            raise ValueError("limit must be a positive integer")

        rows, cols = self.weight_logs_table_actions.get_recent_weights_display(username, int(limit))
        return rows, cols

    # Ths method gets the full history for weight_history.html page
    def get_weight_history_display(self, username: str) -> Tuple[List[Tuple], List[str]]:
        """
        Docstring for get_weight_history_display
        Ths method gets the full history for weight_history.html page
        returns data in a user friendly table format
        :param self: Description
        :param username: Description
        :type username: str
        :return: Description
        :rtype: Tuple[List[Tuple], List[str]]
        """
        if not username or not username.strip():
            raise ValueError("username cannot be empty")

        rows, cols = self.weight_logs_table_actions.get_weight_history_display(username)
        return rows, cols

# This class manages WorkoutSessionsDal interactions
class WorkoutSessionService:
    def __init__(self, workout_sessions_table_actions: dal.WorkoutSessionsDal):
        self.workout_sessions_table_actions = workout_sessions_table_actions

    def get_workout_history_display(self, username: str) -> Tuple[List[Tuple], List[str]]:
        """
        Returns ALL workout sessions for a user with user friendly column names.
        Used by workout history page.
        """
        if not username or not username.strip():
            raise ValueError("username cannot be empty")

        rows, cols = self.workout_sessions_table_actions.get_workout_history_display(username)
        return rows, cols

    def get_recent_workouts_display(self, username: str, limit: int = 10) -> Tuple[List[Tuple], List[str]]:
        if not username or not username.strip():
            raise ValueError("username cannot be empty")
        if limit is None or int(limit) <= 0:
            raise ValueError("limit must be a positive integer")

        rows, cols = self.workout_sessions_table_actions.get_recent_workouts_display(username, int(limit))
        return rows, cols

    # This method gets all rows from the workout_sessions db table
    def get_all_workout_sessions(self) -> Tuple[List[Tuple], List[str]]:
        # Getting all rows from workout_sessions table
        rows, column_names = self.workout_sessions_table_actions.get_all_rows()
        return rows, column_names

    # This method adds a workout entry to the workout_sessions table
    def add_workout_session(
            self, username: str, exercise: str, date_time: str,
            duration_in_minutes: int, sets: int, reps: int, weight: int, notes: Optional[int] = None) -> Tuple[List[Tuple], List[str]]:

        # validating inputs
        if not isinstance(duration_in_minutes, (int, float)):
            raise ValueError(
                f"Workout length must be a number")
        if not isinstance(sets, int):
            raise ValueError(
                f"Sets must be a number")
        if not isinstance(reps, int):
            raise ValueError(
                f"Reps must be a number")
        if not isinstance(weight, (int, float)):
            raise ValueError(
                f"Weight must be a number")

        # calling log user workout procedure to add a workout to workout_sessions table
        rows, column_names = self.workout_sessions_table_actions.log_user_workout_proc(
            username, exercise, date_time, duration_in_minutes, notes, sets, reps, weight)
        return rows, column_names
