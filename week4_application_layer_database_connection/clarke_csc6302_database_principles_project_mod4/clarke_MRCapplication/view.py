
import pandas as pd
import mysql.connector
from typing import List, Tuple
from getpass import getpass
import dal
import bll


# Prompts user for DB connection
def prompt_for_connection():
    host = getpass("Host: ")
    user = getpass("User: ")
    port = int(getpass("Port: "))
    database = getpass("Database: ")
    password = getpass("Password: ")
    return host, user, port, database, password

# This method formats output
def output_separator(input_text: str) -> str:
    """
    - This method formats text and outputs it with separators.
    - Returns a string.
    """
    print("\n" + "="*50)
    print(f" {input_text} ")
    print("="*50)


# This function handles converting the SQL output to a dataframe
def make_dataframe(rows: List, column_names: List) -> str:
    """
    - Converts query output to a dataframe.
    - returns a str.
    """
    # Using pandas to convert data to dataframe, also using to string method to remove index.
    df = pd.DataFrame(rows, columns=column_names)
    print(df.to_string(index=False, justify='center'))

# display total revenue by vessel
def total_rev_by_vess(mrc_app_service):
    # print(f"\nGetting total revenue by vessel ...")
    # making call to db
    rows, column_names = mrc_app_service.view_total_rev_by_vessel()
    # displaying data
    make_dataframe(rows, column_names)


# This method gets a vessel id that matches
def get_vess_id_match(mrc_service_app):
    vessel_name = "Ocean Voyager"
    # print(f"\nGetting vessel ID for {vessel_name}")
    # making call to db
    rows, column_names = mrc_service_app.view_vessel_id_match(vessel_name)
    # displaying data
    print(f"{vessel_name} ID was successfully retrieved ID#:{rows[0][0]}")

# This method gets a NO MATCH vessel id
def get_vess_id_no_match(mrc_service_app):
    # print(f"\nGetting vessel ID with NO match")
    vessel_name = "Big Boat"
    # making call to db
    rows, column_names = mrc_service_app.view_vessel_id_no_match(vessel_name)
    # displaying data
    print(f"{vessel_name} was not found and {rows[0][0]} was returned")

# This method adds new trip details
def add_new_trip(mrc_service_app):
    # params for each db call
    vessel_name = "Wave Rider"
    cost_per_hr = 150
    first_name = "Barry"
    last_name = "Allen"
    phone = "212-312-4567"
    date = "2025-06-30"
    time = "12:00:00"
    trip_length = 3
    total_passengers = 5

    # print(f"\nAdding new trip details to the trip table")
    # adding new passenger to passenger table
    rows, column_names = mrc_service_app.add_passenger(
        first_name, last_name, phone)

    # adding new vessel to vessels table
    rows, column_names = mrc_service_app.add_vessel(vessel_name, cost_per_hr)

    # making call to db
    rows, column_names = mrc_service_app.add_new_trip_details(
        vessel_name, first_name, last_name, date, time, trip_length, total_passengers)
    return rows, column_names

# Getting and displaying all trip views data
def get_view_all_trips(mrc_service_app) -> Tuple[List[Tuple], List[str]]:
    # print(f"\nGetting all trips from the 'All Trips' view")
    rows, column_names = mrc_service_app.view_get_all_trips()
    make_dataframe(rows, column_names)

# This is where the magic happens
def main():
    try:
        #The view should prompt the user for their database parameters and initiate the connection.
        output_separator("Welcome to MRC ...")
        # print(f"Welcome to MRC ...\n")
        output_separator("Please enter your database connection information ...")
        # print(f"Please enter your database connection information ...\n")
        host, user, port, database, password = prompt_for_connection()

        print(f"\nAttempting to connect to the {database} database ....\n")
        # Createing DB connection
        connection = dal.ManageDbConnection(host, user, port, database, password)
        # Connecting to DB
        connection.connect_to_db()

        # Checking if DB was connected
        if connection.get_connection_status():
            print(f"{database} database connection established ...\n")

        # Passing connection to DatabaseActions
        db_actions = dal.DatabaseActions(connection)

        # Passing DAL to BLL services
        vessel_service = bll.VesselService(dal.VesselsDal(db_actions))
        passenger_service = bll.PassengerService(dal.PassengersDal(db_actions))
        trip_service = bll.TripService(dal.TripsDal(db_actions))
        mrc_app_service = bll.MRCAppService(
            vessel_service, trip_service, passenger_service)
        
        # Call the 'Total Revenue by Vessel' view and displays the data in a user friendly way.
        output_separator("Getting total revenue by vessel ...")
        total_rev_by_vess(mrc_app_service)
        
        #Calls the getVesselID function with a match
        output_separator("Getting vessel ID")
        get_vess_id_match(mrc_app_service)

        # Calls the getVesselID function without a match
        output_separator("Getting vessel ID with NO match")
        get_vess_id_no_match(mrc_app_service)

        # Calls the addTrip procedure adding a new trip with a brand new vessel and brand new passenger
        output_separator("Adding new trip details to the trip table")
        rows, column_names = add_new_trip(mrc_app_service)

        # Validating output to confirm if trip details were added or already exist
        if rows:
            print(f"Trip details added successfully")
        
        if rows == 0:
            print(f"Details not added, user or vessel already exists")

        if rows == -1:
            print(f"Vessel was not found")
        
        if rows == -2:
            print(f"Passenger was not found")

        if rows == -3:
            print(f"Vessel and passenger were not found")


        #Calls the 'All Trips' view and displays the data in a user friendly way
        output_separator("Getting all trips from the 'All Trips' view")
        get_view_all_trips(mrc_app_service)

    except mysql.connector.Error as err:
        print(err)


if __name__ == "__main__":
    main()
