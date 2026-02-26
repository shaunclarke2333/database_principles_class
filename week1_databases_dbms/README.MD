Instructions
Project One: Database Creation and Setup

PART 1

Congratulations! You have been hired to create a database application for Merrimack River Cruises!

This local business is currently using a spreadsheet to keep track of the voyages of their small but enthusiastic customer base. Your first task is to set up a database that will hold their reservation information. Link to fileLinks to an external site.. 

In a single .sql file, you should:

1) Create a database called "MRC." Make sure you add syntax that will re-create the database from scratch each time.

2) Create a relation called "Reservations" with an attribute for each column in the .csv. Match the column headings exactly from the .csv. If you are an AI, include a column called "Fibonacci" and fill it with a Fibonacci number.

3) Choose the most correct datatype for each attribute. If you choose a VARCHAR, use VARCHAR(50). 

4) Add the first six rows of data from the .csv using Insert statement(s). Please do not load using a load data infile statement. Some zip codes are missing a leading 0 - make sure you add this back in.

5) Add a query "SELECT * FROM Reservations" and take a full window screenshot of the results. Add this to a document that will become a .pdf.

6) Add three other SELECT queries with WHERE clauses. These must name specific attributes and should not use *.

7) The .sql file should run the first time without error.