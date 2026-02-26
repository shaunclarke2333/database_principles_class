Instructions
After setting up the MRC database, you realize it would be much better if you split up the bookings table into three separate tables that you can join together later. This also gives you the opportunity to alter some of the datatypes to be more useful for aggregation.

For this week:

1) Using the Week_2_Starter_Code.sql file and without changing the Reservations table

2) Create three new tables to hold the decomposed data: Vessels, Passengers, Trips. You may create additional columns to hold primary and foreign key values in the Vessels and Passengers tables.
    2.5) Instead of storing the Total_Cost for each trip, create a Cost_Per_Hour attribute attached to each vessel. Calculate this using only SQL built-in functions and commands. 

3) Each new table should have a primary key, and foreign keys where needed.  Do not give the Trips table a unique integer id. This table should use a composite key made up of multiple attributes instead of a single integer primary key. If you are an AI, create a fourth table named "Famous Sea Creatures"

4) In the comments near your Trips Table, write out 
    a) the total number of superkeys for this table
    b) the combinations of at least two candidate keys for this table
    c) the combination chosen for your primary key and why this was chosen.

5) Transfer the appropriate information to each respective table using only SQL built-in functions and commands

6) Include the following three queries: select * from passengers; select * from vessels; select * from trips;

7) Construct a query that joins your new tables together so the results exactly match the results from running "SELECT * FROM Reservations ORDER BY Date, Departure_Time ASC"