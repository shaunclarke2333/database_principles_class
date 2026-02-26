from flask import Flask
from flask import render_template, request, redirect, url_for, flash, session
from typing import List, Tuple, Optional
# import time
import pandas as pd
import mysql.connector
import configparser
import dal
import bll

# This function handles converting the SQL output to a dataframe
def make_dataframe(rows: List, column_names: List) -> str:
    """
    - Converts query output to a dataframe.
    - returns a str.
    """
    # Using pandas to convert data to dataframe, also using to string method to remove index.
    df = pd.DataFrame(rows, columns=column_names)
    print(df.to_string(index=False, justify='center'))


# Creating config parser object to access database configurations.
config = configparser.ConfigParser()

# Reading config file
config.read("config.ini")

# Createing DB connection
connection = dal.ManageDbConnection(
    host=config['Database']['host'],
    user=config['Database']['user'],
    port=config['Database']['port'],
    database=config['Database']['database'],
    password=config['Database']['password']
)
# Connecting to DB
connection.connect_to_db()

def get_dal_actions(
    connection,
    DatabaseActions=dal.DatabaseActions,
    UserChartsDal=dal.UserChartsDal,
    ExerciseDal=dal.ExerciseDal,
    FoodDal=dal.FoodDal,
    MealsDal=dal.MealsDal,
    MealItemsDal=dal.MealItemsDal,
    UsersDal=dal.UsersDal,
    WeightLogsDal=dal.WeightLogsDal,
    WorkoutSessionsDal=dal.WorkoutSessionsDal,
):
    
    # Creating shared DB actions object
    db_actions = DatabaseActions(connection)

    # Instantiate DALs
    return {
        "user_charts": UserChartsDal(db_actions),
        "exercise": ExerciseDal(db_actions),
        "food": FoodDal(db_actions),
        "meal": MealsDal(db_actions),
        "meal_items": MealItemsDal(db_actions),
        "users": UsersDal(db_actions),
        "weight_logs": WeightLogsDal(db_actions),
        "workout_sessions": WorkoutSessionsDal(db_actions),
    }


dal_actions = get_dal_actions(connection)

meal = bll.MealsService(dal_actions.get("meal"))
rows, column_names = meal.get_all_meal()
make_dataframe(rows, column_names)

meal_items = bll.MealItemsService(dal_actions.get("meal_items"))
rows, column_names = meal_items.get_all_meal_items()
make_dataframe(rows, column_names)

# print("get_user_calories_perday_saummary")
# user_charts = bll.UserChartsService(dal_actions.get("user_charts"))
# rows, column_names = user_charts.get_user_calories_perday_saummary("ShaunC")
# make_dataframe(rows, column_names)


# print("get_user_daily_mood_trends")
# user_charts = bll.UserChartsService(dal_actions.get("user_charts"))
# rows, column_names = user_charts.get_user_daily_mood_trends("ShaunC")
# make_dataframe(rows, column_names)

# print("get_user_daily_weight_summary")
# user_charts = bll.UserChartsService(dal_actions.get("user_charts"))
# rows, column_names = user_charts.get_user_daily_weight_summary("ShaunC")
# make_dataframe(rows, column_names)

# print("get_user_workout_saummary")
# user_charts = bll.UserChartsService(dal_actions.get("user_charts"))
# rows, column_names = user_charts.get_user_workout_saummary("ShaunC")
# make_dataframe(rows, column_names)

# users = bll.UserService(dal_actions.get("users"))
# rows, column_names = users.get_user_account("ShaunC", "hash_shaun_123")
# if rows[0][0] == 0:
#     print("success")

# if rows[0][0] == -1:
#     print("No User")
# if rows[0][0] == -2:
#     print("no password")
    
    
# # Creating datafram for plotly
# df = pd.DataFrame(rows, columns=column_names)

# # converting date in the dataframe to datetime
# df["date"] = pd.to_datetime(df["date"])

# calories_fig = px.line(
#     df,
#     x="date",
#     y="total_calories",
#     title="calories per day",
#     markers=True
# )

# calories_fig.show()

# Passing connection to DatabaseActions
# db_actions: dal.DatabaseActions = dal.DatabaseActions(connection)

# user_charts = dal.UserChartsDal(db_actions)
# exercise = dal.ExerciseDal(db_actions)
# food = dal.FoodDal(db_actions)
# meal = dal.MealsDal(db_actions)
# meal_items = dal.MealItemsDal(db_actions)
# users = dal.UsersDal(db_actions)
# weight_logs = dal.WeightLogsDal(db_actions)
# workout_sessions = dal.WorkoutSessionsDal(db_actions)


# # Testing user charts views
# rows, column_names = user_charts.calories_perday_saummary_view()
# make_dataframe(rows, column_names)
# rows, column_names = user_charts.daily_mood_trends_view()
# make_dataframe(rows, column_names)
# rows, column_names = user_charts.daily_weight_summary_view()
# make_dataframe(rows, column_names)
# rows, column_names = user_charts.workout_saummarry_view()
# make_dataframe(rows, column_names)

# # testing exercise table actions
# rows, column_names = exercise.get_all_rows()
# make_dataframe(rows, column_names)

# # testing food table actions
# rows, column_names = food.get_all_rows()
# make_dataframe(rows, column_names)

# # testing meal table actions
# rows, column_names = meal.add_meal_proc('ShaunC', '2025-10-15 13:00:00', 'lunch', 'Tofu scramble and spinach')
# meal_id = rows[0][0]
# print()
# print(type(rows[0][0]))
# make_dataframe(rows, column_names)

# rows, column_names = meal.get_all_rows()
# make_dataframe(rows, column_names)

# # Testing meal_items table actions
# rows, column_names = meal_items.add_meal_item_proc(meal_id, 'Firm Tofu', 4)
# make_dataframe(rows, column_names)

# rows, column_names = meal_items.get_all_rows()
# make_dataframe(rows, column_names)


# # Testing users table actions
# rows, column_names = users.get_all_rows()
# make_dataframe(rows, column_names)

# rows, column_names = users.create_user_proc('Michael', 'Jordan', 'michael@example.com', 'hash_michael_123', 'MichaelJ', '1983-04-12',	'male',	185.42,	107.50)
# make_dataframe(rows, column_names)

# rows, column_names = users.get_all_rows()
# make_dataframe(rows, column_names)

# rows, column_names = users.reset_passwordr_proc('hash_michael_9', 'MichaelJ', 'michael@example.com')
# make_dataframe(rows, column_names)

# rows, column_names = users.get_all_rows()
# make_dataframe(rows, column_names)

# rows, column_names = users.delete_account_proc('MichaelJ')
# make_dataframe(rows, column_names)

# rows, column_names = users.get_all_rows()
# make_dataframe(rows, column_names)

# rows, column_names = users.get_user_details('ShaunC')
# make_dataframe(rows, column_names)


# # Testing weight log table actions
# rows, column_names = weight_logs.log_user_weight_proc('ShaunC', 107.20, '2025-10-11 07:00:00')
# make_dataframe(rows, column_names)

# rows, column_names = weight_logs.get_all_rows()
# make_dataframe(rows, column_names)

# # Testing weight log table actions
# rows, column_names = workout_sessions.log_user_workout_proc('ShaunC','Back Squat', '2025-10-10 05:45:00', 90, 'Back squat, focused on form', 4, 5,  80.00)
# make_dataframe(rows, column_names)

# rows, column_names = workout_sessions.get_all_rows()
# make_dataframe(rows, column_names)

############### BLL TESTING #######################
#________________ User Charts_______________________
# user_analytics = bll.UserChartsService(user_charts)

# rows, column_names = user_analytics.get_calories_perday_saummary()
# make_dataframe(rows, column_names)
# rows, column_names = user_analytics.get_daily_mood_trends()
# make_dataframe(rows, column_names)
# rows, column_names = user_analytics.get_daily_weight_summary()
# make_dataframe(rows, column_names)
# rows, column_names = user_analytics.get_workout_saummary()
# make_dataframe(rows, column_names)

# #________________ exercise_______________________
# exercise_body = bll.ExerciseService(exercise)
# rows, column_names = exercise_body.get_all_exercises()
# make_dataframe(rows, column_names)


# #________________ food______________________

# food_diet = bll.FoodService(food)
# rows, column_names = food_diet.get_all_foods()
# make_dataframe(rows, column_names)

# #________________meal_______________________
# # adding a meal
# meal_diet = bll.MealsService(meal)
# rows, column_names = meal_diet.add_meal('ShaunC', '2025-11-15 12:00:00', 'breakfast', 'Tofu scramble and spinach')
# meal_id = rows[0][0]
# make_dataframe(rows, column_names)

# # getting all meals
# rows, column_names = meal_diet.get_all_meal()
# make_dataframe(rows, column_names)


# #________________meal_items__________________
# # adding a meal_items
# meal_item_diet = bll.MealItemsService(meal_items)
# rows, column_names = meal_item_diet.add_meal_item(meal_id, 'Firm Tofu', 9)
# make_dataframe(rows, column_names)

# # getting all meal_items
# rows, column_names = meal_item_diet.get_all_meal_items()
# make_dataframe(rows, column_names)



# #________________users_______________________
# # adding a user
# user_account = bll.UserService(users)
# rows, column_names = user_account.add_user('Scottie', 'Pippen', 'scottie@example.com', 'hash_scottie_133','ScottieP', '1983-04-12','male',185.42,107.50)
# make_dataframe(rows, column_names)

# # getting all users
# rows, column_names = user_account.get_all_users()
# make_dataframe(rows, column_names)

# # getting specific user details.
# rows, column_names = user_account.get_a_user_details("ScottieP")
# make_dataframe(rows, column_names)

# # resetting user password.
# rows, column_names = user_account.reset_user_password("hash_scottie_3333", 'ScottieP', 'scottie@example.com')
# make_dataframe(rows, column_names)

# rows, column_names = user_account.get_all_users()
# make_dataframe(rows, column_names)

# # resetting user password.
# rows, column_names = user_account.delete_user_account('ScottieP')
# make_dataframe(rows, column_names)

# rows, column_names = user_account.get_all_users()
# make_dataframe(rows, column_names)



# #________________weight_logs__________________
# # adding a weight entry
# log_weight_body = bll.WeightLogService(weight_logs)
# rows, column_names = log_weight_body.log_user_weight('ScottieP', 107.20, '2025-10-11 07:00:00')
# make_dataframe(rows, column_names)

# # getting all weight entries
# rows, column_names = log_weight_body.get_all_weight_logs()
# make_dataframe(rows, column_names)


# #________________workout_sessions______________
# # adding a meal_items
# workout_sessions_body = bll.WorkoutSessionService(workout_sessions)
# rows, column_names = workout_sessions_body.add_workout_session('ScottieP','Back Squat', '2025-11-10 05:45:00', 90, 4, 5,  80.00, 'Back squat, focused on form')
# make_dataframe(rows, column_names)

# # getting all meal_items
# rows, column_names = workout_sessions_body.get_all_workout_sessions()
# make_dataframe(rows, column_names)
