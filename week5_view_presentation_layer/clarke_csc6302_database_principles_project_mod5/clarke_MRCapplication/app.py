from flask import Flask
from flask import render_template, request, redirect, url_for, flash, session
from typing import List, Tuple
# import time
import pandas as pd
import mysql.connector
import configparser
import dal
import bll


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

# Passing connection to DatabaseActions
db_actions: dal.DatabaseActions = dal.DatabaseActions(connection)

# Passing DAL to BLL services
vessel_service = bll.VesselService(dal.VesselsDal(db_actions))
passenger_service = bll.PassengerService(dal.PassengersDal(db_actions))
trip_service = bll.TripService(dal.TripsDal(db_actions))

# rows, column_names = trip_service.get_view_all_trips()
# print(make_dataframe(rows, column_names))

# Creating the web app
app = Flask(__name__)

# Creating dummy secret key for login sessions
app.secret_key = "just-a-dummy-key"


# Creating homepage route
@app.route("/")
def home():
    username = session.get("username")  # None if not logged in
    return render_template("index.html", username=username)


# Creating login page route
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

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
            # validate the users credentials
            if username == "admin" and password == "secret":
                # Confimring login to user and starting session with flasj
                flash("Logged in successfully!", "success")
                # Saving authenticated username in session to use throught the session
                session["username"] = username
                
                username = session.get("username")
                # Converting first letter in name to uppercase
                username = username.capitalize()
                # redirecting logged in user to their dashboard
                return redirect(url_for("dashboard"))
            else:
                error = "Invalid username or password."

    # GET or failed POST: re-render form
    return render_template("login.html", error=error)

# Creating logout route
@app.route("/logout")
def logout():
    # Closing session which will logout the user
    session.clear()   
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


# Creating dashboard route
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        flash("Please log in first.")
        return redirect(url_for("login"))
    
    username = session.get("username")
    
    return render_template("dashboard.html", username=username)


# Creating add passenger route with variables needed to add passenger to DB
@app.route("/add-passenger", methods=["GET", "POST"])
def add_passenger():

    # Setting validation error place holder if anything form related fails
    error = None

    if request.method == "POST":
        """
        Stripping whitespace from input.
        using empty quotes to ensure app does not crash
        """  
        first_name: str = request.form.get("first_name", "").strip()
        last_name: str = request.form.get("last_name", "").strip()
        phone: str = request.form.get("phone", "").strip()

        if not first_name or not last_name or not phone:
            error = "First name, Last name and Phone are required"
        else:
            try:
                rows, column_names = passenger_service.add_passenger(first_name, last_name, phone)
                if rows is not None:
                    added_user_id: int = rows[0][0]
                    if isinstance(added_user_id, int):
                        # Confimring Passenger was added and starting session with flasj
                        flash("Passenger added successfully!", "success")
                        #redirecting user back to their dashboard with their username to display
                        username = session.get("username")
                        return redirect(url_for("dashboard", username=username))
                    
                    raise ValueError(f"Passenger was not added")
                else:
                    raise ValueError(f"Passenger was not added")
                    
            except Exception as err:
                error = err
    # return user to add passenger page if passenger was not added
    return render_template("add_passenger.html", error=error)

 
# Creating add vessel route
@app.route("/add-vessel", methods=["GET", "POST"])
def add_vessel():
    
    # Setting validation error place holder if anything form related fails
    error = None

    # Logic to run if the users submits the form
    if request.method == "POST":
        """
        Stripping whitespace from input.
        using empty quotes to ensure app does not crash
        """  
        vessel_name: str = request.form.get("vessel_name", "").strip()
        cost_per_hr_raw: str = request.form.get("cost_per_hr", "").strip()

        if not vessel_name or not cost_per_hr_raw:
            error = "Vessel name and cost per hr are required"
        else:
             # Make sure cost_per_hr is an integer
            try:
                cost_per_hr: int = int(cost_per_hr_raw)
            except ValueError:
                error = "Cost per hour must be a whole number."
            else:
                try:
                    rows, column_names = vessel_service.add_vessel(
                        vessel_name, cost_per_hr
                    )

                    if rows is not None:
                        added_vessel_id: int = rows[0][0]
                        if isinstance(added_vessel_id, int):
                            flash("Vessel added successfully!", "success")
                            username = session.get("username")
                            return redirect(url_for("dashboard", username=username))

                        raise ValueError("Vessel was not added")
                    else:
                        raise ValueError("Vessel was not added")

                except Exception as err:
                    # Convert exception to string so template can show it
                    error = str(err)

    # GET requests and POST requests with any errors handled here
    return render_template("add_vessel.html", error=error)
            

@app.route("/add-trip", methods=["GET", "POST"])
def add_trip():
    error = None

    # Load dropdown data for both GET and POST
    vessels_rows, _ = vessel_service.get_all_vessels()
    passengers_rows, _ = passenger_service.get_all_passengers()

    if request.method == "POST":
        # Read form data
        departure_datetime: str = request.form.get("departure_datetime", "").strip()
        vessel_name: str = request.form.get("vessel_name", "").strip()
        trip_length_raw: str = request.form.get("trip_length", "").strip()
        total_passengers_raw: str = request.form.get("total_passengers", "").strip()
        passenger_value: str = request.form.get("passenger_name", "").strip()

        # Getting passenger first and last name from "first|last"
        first_name = ""
        last_name = ""
        if passenger_value and "|" in passenger_value:
            first_name, last_name = passenger_value.split("|", 1)
            first_name = first_name.strip()
            last_name = last_name.strip()

        # Validating input
        if not (departure_datetime and vessel_name and first_name and last_name and
                trip_length_raw and total_passengers_raw):
            error = "All fields are required."
        else:
            # Split datetime-local into date and time
            try:
                date_part, time_part = departure_datetime.split("T", 1)
            except ValueError:
                error = "Invalid date/time format."
            else:
                # Convert numeric fields
                try:
                    trip_length: int = int(trip_length_raw)
                    total_passengers: int = int(total_passengers_raw)
                except ValueError:
                    error = "Trip length and total passengers must be whole numbers."
                else:
                    # Call BLL to add the trip
                    try:
                        rows, column_names = trip_service.add_trip(
                            vessel_name,
                            first_name,
                            last_name,
                            date_part,
                            time_part,
                            trip_length,
                            total_passengers
                        )

                        if rows:
                            flash("Trip added successfully!", "success")
                            username = session.get("username")
                            return redirect(url_for("dashboard", username=username))
                        else:
                            error = "Trip was not added."
                    except Exception as err:
                        error = str(err)

    # GET requests and POST with errors land here
    return render_template(
        "add_trip.html",
        error=error,
        vessels=vessels_rows,
        passengers=passengers_rows,
    )


@app.route("/all-trips-view")
def all_trips_view():
    rows, column_names = trip_service.get_view_all_trips()
    return render_template("view_all_trips.html", rows=rows, column_names=column_names)


if __name__ == "__main__":
    app.run(debug=True)
