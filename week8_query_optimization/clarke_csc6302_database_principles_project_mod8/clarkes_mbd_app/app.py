"""
Author: Shaun Clarke
Class: CSC6302 Database Principles
Module 08: Final Oroject
"""

from flask import Flask
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from functools import wraps
from datetime import datetime
from typing import List, Tuple
# import time
import pandas as pd
import plotly.express as px
import mysql.connector
import dal
import bll

# This fucntion creates the DAL service objects that talk to the database
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

    # Creating shared DB actions object with active db connection
    db_actions = DatabaseActions(connection)

    # Creating a dictionary of instantiated DAL objects
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

# Creating flask app
app = Flask(__name__)

# Dummy secret key so we can use session features
app.secret_key = "some-dummy-key"

# Theis function gets a database object and allows you to create a connection from the object
def get_db_connection(db_connection_manager_dal=dal.ManageDbConnection):

    # Validating that the DB is connected
    if not session.get("db_connected"):
        raise mysql.connector.Error("DB not connected")

    connection = db_connection_manager_dal(
        host="localhost",
        port=3306,
        user=session.get("db_user"),
        password=session.get("db_pass"),
        database="mbd"
    )

    # connecting database
    connection.connect_to_db()

    # Proceeding to return a DB connection if DB is connected
    return connection


# Creating a decorator to use with routes that require a database connection.
# User gets notified if they try to access specific pages and the DB is not connected.
def deb_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not session.get("db_connected"):
            flash(
                "Database is not connected. Click the DB button in the navbar to connect.", "warning")
            return redirect(url_for("home"))
        return view_func(*args, **kwargs)
    return wrapper


# Creating homepage route
@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

# Creating database connection route
@app.route("/db/connect", methods=["POST"])
def connect_db():
    # Creating json object to fetch entered db creds
    db_info = request.get_json(silent=True) or {}
    db_user = (db_info.get("db_user") or "").strip()
    db_pass = db_info.get("db_pass") or ""

    # error message to handle if db creds were not entered
    if not db_user or not db_pass:
        return jsonify(ok=False, message="Username and password required."), 400

    try:
        # Createing DB connection
        connection = dal.ManageDbConnection(
            host="localhost",
            port=3306,
            user=db_user,
            password=db_pass,
            database="mbd"
        )

        # Connecting to DB
        connection.connect_to_db()

        # checking connection status
        connection_status = connection.get_connection_status()
        if not connection_status:
            raise mysql.connector.Error(f"Database connection failed")

        # If connection status check passed, update db_conected in session to true for DB sessions state and add the db user and pass to session
        # This allows the connection to persist for the session
        # This is not best practice to store password in session, i am only doing it for this project and due to time constraints.
        session["db_connected"] = True
        session["db_user"] = db_user
        session["db_pass"] = db_pass

        # Returning JSON object
        return jsonify(ok=True)

    except Exception:
        # Removing everything from session to cleanup and reset session state
        session.pop("db_connected", None)
        session.pop("db_user", None)
        session.pop("db_pass", None)
        # Returning a json object with error message
        return jsonify(ok=False, message="Invalid DB credentials."), 401


# Creating signin route
@app.route("/signin", methods=["GET", "POST"])
# Alerts the user if they try to do anything befor connecting the DB.
@deb_required
def signin():

    # setting error variable
    error = None
    if session.get("user_id"):
        # redirecting user to dashboard
        return render_template("dashboard.html")

    # Getting user input from login form
    if request.method == "POST":
        """
        Stripping whitespace from input.
        using empty quotes to ensure app does not crash
        """
        username: str = request.form.get("username", "").strip()
        password: str = request.form.get("password", "").strip()

        # Doing server side validation to speed things up.
        if not username or not password:
            error: str = "Username and password are required."
        else:
            # Checking database to validate the users credentials
            try:
                # Getting DB connection
                connection = get_db_connection()
                # Creating database actions
                dal_actions = get_dal_actions(connection)

                #  validating user login
                users = bll.UserService(dal_actions.get("users"))
                rows, column_names = users.get_user_account(username, password)
                if rows[0][0] == 0:
                    # Confimring login to user and starting session with flasj
                    flash("Logged in successfully!", "success")
                    # Saving authenticated username in session to use throught the session
                    session["username"] = username

                    # redirecting user to dashboard
                    return redirect(url_for("dashboard"))
                

            except Exception as e:
                # handling if username or password is incorrect.
                flash(f"Invalid username or password: {e}.", "warning")


    # GET or if POST failed, sednd user back to signin page
    return render_template("signin.html")


# Creating dashboard route
@app.route("/dashboard", methods=["GET"])
@deb_required
def dashboard():

    # Getting DB connection
    connection = get_db_connection()
    # Creating database actions
    dal_actions = get_dal_actions(connection)

    # Creating user chart service object
    user_charts = bll.UserChartsService(dal_actions.get("user_charts"))
    username = session.get("username")

    # Getting logged in users macros and calories from db
    rows, column_names = user_charts.get_user_calories_perday_saummary(username)
    macro_df = pd.DataFrame(rows, columns=column_names)

    macros_pie_chart = None  # Setting default to None in the event a new user has no data

    if not macro_df.empty:
        # formatting date
        macro_df["date"] = pd.to_datetime(macro_df["date"])

        daily_macros = (
            macro_df
            .groupby(["user_id", "username", "date"], as_index=False)
            .agg(
                total_calories=("total_calories", "sum"),
                total_protein=("total_protein", "sum"),
                total_carbs=("total_carbs", "sum"),
                total_fats=("total_fats", "sum"),
                total_meals=("total_meals", "sum"),
            )
            .sort_values("date")
        )

        # mental note: daily_macros can still be empty in edge cases remember to test
        # Logic checks if user has data before attempting to data which might cause errors
        if not daily_macros.empty:
            latest_date = daily_macros["date"].max()

            # getting the latest date to make sure the chart always shows latest data.
            latest_row_df = daily_macros[daily_macros["date"] == latest_date]
            # Making sure that rows are not empty after filtering by latest date
            if not latest_row_df.empty:
                latest_row = latest_row_df.iloc[0]

                # Creating a dataframe with the specific columns needed for the macros chart
                pie_df = pd.DataFrame({
                    "macro": ["Protein", "Carbs", "Fats"],
                    "grams": [
                        float(latest_row["total_protein"] or 0),
                        float(latest_row["total_carbs"] or 0),
                        float(latest_row["total_fats"] or 0),
                    ],
                })

                # Using plotly express to create the pie chart with latest date info
                macro_pie_fig = px.pie(
                    pie_df,
                    names="macro",
                    values="grams",
                    title=f"Macros (grams) — {latest_date.date()}",
                )
                # Centering the chart title and apply margins for chart layout on dashboard
                macro_pie_fig.update_layout(
                    title_x=0.5, margin=dict(l=20, r=20, t=60, b=20)
                )
                # Converting the Plotly chart to html. the jinja template will only accept it in html format.
                macros_pie_chart = macro_pie_fig.to_html(full_html=False)

    # If user has no macro data yet, show an empty placeholder chart
    if not macros_pie_chart:
        # Creating an empty dataframe with the specific columns needed for the macros chart
        pie_df = pd.DataFrame({"macro": ["Protein", "Carbs", "Fats"], "grams": [0, 0, 0]})
        # Generating empty chart
        macro_pie_fig = px.pie(pie_df, names="macro", values="grams", title="Macros (grams) — No data yet")
        # Centering the chart title and apply margins for chart layout on dashboard
        macro_pie_fig.update_layout(title_x=0.5, margin=dict(l=20, r=20, t=60, b=20))
        # Converting the Plotly chart to html. the jinja template will only accept it in html format.
        macros_pie_chart = macro_pie_fig.to_html(full_html=False)

    # getting users weight summary
    rows, column_names = user_charts.get_user_daily_weight_summary(username)
    weight_df = pd.DataFrame(rows, columns=column_names)

    weight_chart = None  # Setting default to None in the event a new user has no data

    if not weight_df.empty:
        # Formatting the date column
        weight_df["date"] = pd.to_datetime(weight_df["date"])
        # sorting by date
        weight_df = weight_df.sort_values("date")

        # Using plotly express to create a line chart that is sorted by date
        weight_fig = px.line(
            weight_df,
            x="date",
            y="user_weight",
            title="Weight Trend",
            markers=True,
        )
        weight_fig.update_layout(title_x=0.5, margin=dict(l=20, r=20, t=60, b=20))
        weight_chart = weight_fig.to_html(full_html=False)

    # If no weight yet, show empty placeholder chart
    if not weight_chart:
        empty_weight_df = pd.DataFrame({"date": [pd.Timestamp.today()], "user_weight": [0]})
        weight_fig = px.line(empty_weight_df, x="date", y="user_weight", title="Weight Trend — No data yet", markers=True)
        weight_fig.update_layout(title_x=0.5, margin=dict(l=20, r=20, t=60, b=20))
        weight_chart = weight_fig.to_html(full_html=False)

    return render_template(
        "dashboard.html",
        macros_pie_chart=macros_pie_chart,
        weight_chart=weight_chart,
    )

# Creating forgot password route
@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    # When button is clicked, the GET method redirects user to the reset form
    if request.method == "GET":
        return render_template("forgot_password.html")

    # When the user submits the form
    email = (request.form.get("email") or "").strip()
    username = (request.form.get("username") or "").strip()
    password = (request.form.get("password") or "").strip()

    # letting the user know if they missed a field.
    if not email or not username or not password:
        return render_template(
            "forgot_password.html",
            error="Email, username, and new password are required."
        )

    try:
        connection = get_db_connection()
        dal_actions = get_dal_actions(connection)

        # creating user service object
        users_service = bll.UserService(dal_actions.get("users"))

        # Calling stored procedure in DB to reset user's password
        rows, _ = users_service.reset_user_password(
            email=email,
            password=password,
            username=username
        )

        """
        Stored procedure output after attempting to reset user password:
          0 success
          1 yser not found
          2 email not found
         -3 email/username mismatch
        """ 
        # parsing tuple of rowas to get returned value
        result_code = rows[0][0] if rows else None

        # Logic to inform user based on code return from stored procedure
        if result_code == -1:
            return render_template(
                "forgot_password.html",
                error="Email not found."
            )
        
        if result_code == -2:
            return render_template(
                "forgot_password.html",
                error="User not found."
            )

        if result_code == -3:
            return render_template(
                "forgot_password.html",
                error="Email and username do not match."
            )

        # Displaying success messsage to user
        flash("Password reset successfully. Please sign in.", "success")
        return redirect(url_for("signin"))

    except Exception as e:
        return render_template(
            "forgot_password.html",
            error=f"Could not reset password: {e}"
        )

# Creating delete account 
@app.route("/delete-account", methods=["GET", "POST"])
@deb_required
def delete_account():
    try:
        # making sure user is signed in
        username = session.get("username")
        if not username:
            flash("Please sign in first.", "warning")
            return redirect(url_for("signin"))

        # loading confirmation page
        if request.method == "GET":
            return render_template("delete_account.html", username=username)

        # making user check a box confirmed deleting account
        confirm = request.form.get("confirm")  # checkbox
        if confirm != "yes":
            flash("Please confirm to delete your account.", "warning")
            return render_template("delete_account.html", username=username)

        # Connecting to database and creating user service object
        connection = get_db_connection()
        dal_actions = get_dal_actions(connection)
        users_service = bll.UserService(dal_actions.get("users"))

        # Calling stored procedure to delete a user account
        rows, cols = users_service.delete_user_account(username)

        # Logic to interpret result safely
        result = rows[0][0] if rows and len(rows[0]) else None

        """
        What the delete user stored procedure returns
        0 = deleted OK
        -1 = user not found
        """

        if result == -1:
            flash("User not found.", "danger")
            return render_template("delete_account.html", username=username)

        if result not in (0, 1) and (result is None):
            flash("Could not delete account. Please try again.", "danger")
            return render_template("delete_account.html", username=username)

        # if account was successfully deleted, clear session and redirect user to home
        session.clear()
        flash("Your account has been deleted.", "success")
        return redirect(url_for("home"))

    except Exception as e:
        flash(f"Could not delete account: {e}", "danger")
        return redirect(url_for("account_settings"))



@app.route("/signup", methods=["GET", "POST"])
@deb_required
def signup():

    if request.method == "GET":
        return render_template("signup.html")
    
    # Getting data entered into all form fields
    username = (request.form.get("username") or "").strip()
    email = (request.form.get("email") or "").strip()
    password = (request.form.get("password") or "").strip()

    first_name = (request.form.get("first_name") or "").strip()
    last_name = (request.form.get("last_name") or "").strip()
    dob = (request.form.get("dob") or "").strip()
    gender = (request.form.get("gender") or "").strip()

    height_raw = (request.form.get("height") or "").strip()
    weight_raw = (request.form.get("weight") or "").strip()
    
    # All or nothing validation making sure all required fields exist
    if not all([first_name, last_name, username, email, password, dob, gender, height_raw, weight_raw]):
        return render_template("signup.html", error="All fields are required.")

    # Making sure height and weight are not 0 and converting themt o floats
    try:
        height = float(height_raw)
        weight = float(weight_raw)
        if height <= 0 or weight <= 0:
            return render_template("signup.html", error="Height and weight must be greater than 0.")
    except ValueError:
        return render_template("signup.html", error="Height and weight must be valid numbers.")

    try:
        # connecting to database 
        connection = get_db_connection()
        
        # creating db actions  object
        dal_actions = get_dal_actions(connection)
        # creating user servie object
        users_service = bll.UserService(dal_actions.get("users"))  

        #  Calling procedure to add user to DB
        rows, _ = users_service.add_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            username=username,
            dob=dob,
            gender=gender,
            height=height,
            weight=weight
        )

        #  if nothing was returned inform user that account was not created
        if not rows or not rows[0] or rows[0][0] is None:
            return render_template("signup.html", error="Could not create account. Please try again.")

        # Getting the output of the stored procedure that created the account
        created_id = int(rows[0][0])

        # Validating the output code
        if created_id == -1:
            return render_template("signup.html", error="That username is already taken.")
        if created_id == -2:
            return render_template("signup.html", error="That email is already in use.")
        if created_id <= 0:
            return render_template("signup.html", error="Could not create account. Please try again.")

        flash("Account created. Please sign in.", "success")
        return redirect(url_for("signin"))

    except Exception as e:
        return render_template("signup.html", error=f"Could not create account: {e}")


# Creatiing logout route
@app.route("/logout", methods=["GET"])
def logout():
    # Closing session which will logout the user
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("signin"))

# Creatinf account settings route
@app.route("/account", methods=["GET"])
# Alerts the user if they try to do anything befor connecting the DB.
@deb_required
def account_settings():
    return render_template("account_settings.html")


@app.route("/workout/log", methods=["GET", "POST"])
def workout_log():
    # Empty list to hold exercise and sessions data from DB
    exercises = []
    sessions = []
    # getting the present date and time 
    now_local = datetime.now().strftime("%Y-%m-%dT%H:%M")

    # Getting username that was stored in session
    username = session.get("username")
    if not username:
        flash("Please sign in first.", "warning")
        return redirect(url_for("signin"))

    try:
        connection = get_db_connection()
        dal_actions = get_dal_actions(connection)

        exercise_service = bll.ExerciseService(dal_actions.get("exercise"))
        workout_service = bll.WorkoutSessionService(dal_actions.get("workout_sessions"))

        # Load exercises for dropdown
        ex_rows, ex_cols = exercise_service.get_all_exercises()
        exercises = [dict(zip(ex_cols, r)) for r in ex_rows]

        # Load recent workouts
        ws_rows, ws_cols = workout_service.get_recent_workouts_display(username, limit=10)
        sessions = [dict(zip(ws_cols, r)) for r in ws_rows]

        if request.method == "POST":
            try:
            #  when the user clicks the button, get all form data
                exercise_name = request.form["exercise_name"]
                session_datetime = request.form["session_datetime"]
                duration = int(request.form["duration_minutes"])
                sets = int(request.form["sets"])
                reps = int(request.form["reps"])
                weight = float(request.form["weight"])
                notes = request.form.get("notes") or None

                # Adding workout to DB
                workout_service.add_workout_session(
                    username=username,
                    exercise=exercise_name,
                    date_time=session_datetime,
                    duration_in_minutes=duration,
                    sets=sets,
                    reps=reps,
                    weight=weight,
                    notes=notes
                )

                flash("Workout logged successfully.", "success")
                return redirect(url_for("workout_log"))

            except ValueError:
                flash("Please enter valid numeric values.", "danger")

    except Exception as e:
        flash(f"Could not load workout page: {e}", "danger")

    return render_template(
        "workout_log.html",
        exercises=exercises,
        sessions=sessions,
        now_local=now_local
    )


@app.route("/workout/history", methods=["GET"])
def workout_history():
    try:
        # Getting username that was stored in session
        username = session.get("username")
        if not username:
            flash("Please sign in first.", "warning")
            return redirect(url_for("signin"))

        connection = get_db_connection()
        dal_actions = get_dal_actions(connection)

        workout_service = bll.WorkoutSessionService(dal_actions.get("workout_sessions"))

        # Getting the users workout history from DB
        rows, cols = workout_service.get_workout_history_display(username)
        # Using list comprehension to make a list of dictionaries with the DB rows that were returned
        sessions = [dict(zip(cols, r)) for r in rows]

        return render_template("workout_history.html", sessions=sessions)

    except Exception as e:
        flash(f"Could not load workout history: {e}", "danger")
        return render_template("workout_history.html", sessions=[])


@app.route("/meals/create", methods=["GET", "POST"])
def meal_create():
    # Empty list to hold todays items.
    today_items = []
    # Getting present date and time
    now_local = datetime.now().strftime("%Y-%m-%dT%H:%M")

    if request.method == "POST":
        # Getting form data
        meal_date = (request.form.get("meal_datetime") or "").strip()
        meal_type = (request.form.get("meal_type") or "").strip()
        notes = (request.form.get("notes") or "").strip()

        # if all fields are not populated
        if not meal_date or not meal_type or not notes:
            flash("Meal date/time, meal type, and notes are required.", "warning")
        else:
            try:
                username = session.get("username")
                # Making sure user is signed in.
                if not username:
                    flash("Please sign in first.", "warning")
                    return redirect(url_for("signin"))

                connection = get_db_connection()
                dal_actions = get_dal_actions(connection)
                meal_service = bll.MealsService(dal_actions.get("meal"))

                # Adding meal to DB
                rows, _ = meal_service.add_meal(username, meal_date, meal_type, notes)
                meal_id = rows[0][0]

                flash("Meal created. Please add meal items.", "success")
                return redirect(url_for("meal_add_items", meal_id=meal_id))
            except Exception as e:
                flash(f"Could not create meal: {e}", "danger")

    # Making sure todays item table data always loads
    try:
        username = session.get("username")
        if username:
            connection = get_db_connection()
            dal_actions = get_dal_actions(connection)
            meal_items_service = bll.MealItemsService(dal_actions.get("meal_items"))

            # Getting the date right now
            today = datetime.now().date()

            # Getting the meals items entered today for a specific user.
            rows, cols = meal_items_service.get_today_items_for_user(username, today)
            today_items = [dict(zip(cols, r)) for r in rows]
    except Exception:
        pass

    return render_template(
        "meal_create.html",
        today_items=today_items,
        now_local=now_local
    )



@app.route("/meals/<int:meal_id>/items", methods=["GET", "POST"])
def meal_add_items(meal_id: int):
    food_list = []
    current_items = []
    meal_info = None

    try:
        username = session.get("username")
        if not username:
            flash("Please sign in first.", "warning")
            return redirect(url_for("signin"))

        connection = get_db_connection()
        dal_actions = get_dal_actions(connection)

        food_service = bll.FoodService(dal_actions.get("food"))
        meal_items_service = bll.MealItemsService(dal_actions.get("meal_items"))
        meal_service = bll.MealsService(dal_actions.get("meal"))

        if request.method == "POST":
            # Getting form data when user submits the form
            food_name = (request.form.get("food_name") or "").strip()
            servings_raw = (request.form.get("servings") or "").strip()

            # making sure all fields are populated
            if not food_name or not servings_raw:
                flash("Food and servings are required.", "warning")
                return redirect(url_for("meal_add_items", meal_id=meal_id))

            try:
                # Making sure servings is not less than 0
                servings = float(servings_raw)
                if servings <= 0:
                    raise ValueError()
            except ValueError:
                flash("Servings must be a valid number greater than 0.", "warning")
                return redirect(url_for("meal_add_items", meal_id=meal_id))

            # Adding meal items to (meal) to DB
            meal_items_service.add_meal_item(meal_id, food_name, servings)
            flash("Item added.", "success")
            return redirect(url_for("meal_add_items", meal_id=meal_id))

        # Get method also loads dropdown foods
        food_rows, food_cols = food_service.get_all_foods()
        food_list = [dict(zip(food_cols, r)) for r in food_rows]

        # Getting items for the meal that was just added
        current_rows, current_cols = meal_items_service.get_items_for_meal(username, meal_id)
        current_items = [dict(zip(current_cols, r)) for r in current_rows]

        # Getting meal fro specific user
        meal_rows, meal_cols = meal_service.get_meal_by_id(username, meal_id)
        # Creating a dictionary of lists with returned data.
        meal_info = dict(zip(meal_cols, meal_rows[0])) if meal_rows else None

    except Exception as e:
        flash(f"Could not load meal items screen: {e}", "danger")

    return render_template(
        "meal_add_items.html",
        meal_id=meal_id,
        food_list=food_list,
        current_items=current_items,
        meal_info=meal_info,
    )


@app.route("/weight/log", methods=["GET", "POST"])
def weight_log():
    weights = []

    try:
        username = session.get("username")
        if not username:
            flash("Please sign in first.", "warning")
            return redirect(url_for("signin"))

        connection = get_db_connection()
        dal_actions = get_dal_actions(connection)
        weight_service = bll.WeightLogService(dal_actions.get("weight_logs"))

        if request.method == "POST":
            # Getting data from form when user hits submit
            weight_datetime = (request.form.get("weight_datetime") or "").strip()
            weight_raw = (request.form.get("weight") or "").strip()

            # The weight field is required and manually entered so handling conversion error
            try:
                # Conerting entered weight to float.
                weight_val = float(weight_raw)
            except ValueError:
                flash("Weight must be a valid number.", "warning")
                return redirect(url_for("weight_log"))

            # Adding user's weight to DB
            weight_service.log_user_weight(username, weight_val, weight_datetime)

            flash("Weight logged.", "success")
            return redirect(url_for("weight_log"))

        #Get method show 10 recent weigh-ins from DB
        rows, cols = weight_service.get_recent_weights_display(username, limit=10)
        weights = [dict(zip(cols, r)) for r in rows]

    except Exception as e:
        flash(f"Could not load weight log page: {e}", "danger")

    return render_template("weight_log.html", weights=weights)



@app.route("/weight/history", methods=["GET"])
def weight_history():
    weights = []

    try:
        username = session.get("username")
        if not username:
            flash("Please sign in first.", "warning")
            return redirect(url_for("signin"))

        connection = get_db_connection()
        dal_actions = get_dal_actions(connection)
        weight_service = bll.WeightLogService(dal_actions.get("weight_logs"))

        rows, cols = weight_service.get_weight_history_display(username)
        weights = [dict(zip(cols, r)) for r in rows]

    except Exception as e:
        flash(f"Could not load weight history: {e}", "danger")

    return render_template("weight_history.html", weights=weights)



if __name__ == "__main__":
    app.run(debug=True)
