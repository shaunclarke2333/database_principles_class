/*
Each time this script is ran it will drop the database if it already exists.
Mental Note: This workflow is not for production. Only required for weekly assignments.
*/
DROP DATABASE IF EXISTS `mbd`;
-- Creating the database that will be used
CREATE DATABASE IF NOT EXISTS `mbd`;
-- Making the databse we want to work with active and ready for crud operations
USE `mbd`;

-- Dropping table if it already exists
DROP TABLE IF EXISTS `users`;

-- creating users table
CREATE TABLE `users` (
  `user_id` INT AUTO_INCREMENT PRIMARY KEY,
  `first_name` VARCHAR(50),
  `last_name` VARCHAR(50),
  `email` VARCHAR(150) UNIQUE,
  `password_hash` VARCHAR(255),
  `created_at` DATETIME,
  `username` VARCHAR(100) UNIQUE,
  `date_of_birth` DATE,
  `gender` ENUM('male','female','nonbinary','other'),
  `height` DECIMAL(5,2),
  `weight` DECIMAL(5,2)
);

-- Dropping table if it already exists
DROP TABLE IF EXISTS `weight_logs`;

-- creating weight_logs table
CREATE TABLE `weight_logs` (
  `weight_id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT,
  `weight` DECIMAL(5,2),
  `weight_datetime` DATETIME,
  FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Dropping table if it already exists
DROP TABLE IF EXISTS `exercises`;

-- creating exercises table
CREATE TABLE `exercises` (
  `exercise_id` INT AUTO_INCREMENT PRIMARY KEY,
  `exercise_name` VARCHAR(100),
  `exercise_category` VARCHAR(50),
  `muscle_group` VARCHAR(50)
);


-- Dropping table if it already exists
DROP TABLE IF EXISTS `meals`;

-- creating meals table
CREATE TABLE `meals` (
  `meal_id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT,
  `meal_datetime` DATETIME,
  `meal_type` ENUM('breakfast','lunch','dinner','snack'),
  `notes` TEXT NULL,
  FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Dropping table if it already exists
DROP TABLE IF EXISTS `food`;

-- creating food table
CREATE TABLE `food` (
  `food_id` INT AUTO_INCREMENT PRIMARY KEY,
  `food_name` VARCHAR(100),
  `brand` VARCHAR(100) NULL,
  `serving_size_amount` DECIMAL(6,2),
  `serving_size_unit` VARCHAR(200),
  `calories_per_serving` INT,
  `protein` DECIMAL(6,2),
  `carbs` DECIMAL(6,2),
  `fat` DECIMAL(6,2)
);

-- Dropping table if it already exists
DROP TABLE IF EXISTS `meal_items`;

-- creating meal_items table
CREATE TABLE `meal_items` (
  `meal_item_id` INT AUTO_INCREMENT PRIMARY KEY,
  `meal_id` INT,
  `food_id` INT,
  `servings` DECIMAL(5,2),
  FOREIGN KEY (`meal_id`) REFERENCES `meals` (`meal_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`food_id`) REFERENCES `food` (`food_id`) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Dropping table if it already exists
DROP TABLE IF EXISTS `mood_entries`;

-- creating mood_entries table
CREATE TABLE `mood_entries` (
  `mood_id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT,
  `entry_datetime` DATETIME,
  `mood_score` TINYINT,
  `energy_level` TINYINT NULL,
  `stress_level` TINYINT NULL,
  `note` TEXT,
  FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Dropping table if it already exists
DROP TABLE IF EXISTS `workout_sessions`;

-- creating workout_sessions table
CREATE TABLE `workout_sessions` (
  `session_id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT,
  `exercise_id` INT,
  `session_datetime` DATETIME,
  `duration_minutes` INT,
  `notes` TEXT NULL,
  `sets` INT NULL,
  `reps` INT NULL,
  `weight` DECIMAL(6,2) NULL,
  FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`exercise_id`) REFERENCES `exercises` (`exercise_id`) ON DELETE CASCADE ON UPDATE CASCADE
);


-- ****** Inserting sample data for my mbd wellness app database ******


/* ---------- USERS (10 rows) ---------- */
INSERT INTO users
  (first_name, last_name, email, password_hash, created_at, username, date_of_birth, gender, height, weight)
VALUES
  ('Shaun', 'Clarke', 'shaun@example.com',    'hash_shaun_123', '2025-10-01 07:30:00', 'ShaunC',     '1983-04-12', 'male',      185.42, 107.50),
  ('Alicia', 'Brown', 'alicia.b@example.com','hash_alicia_456','2025-10-02 08:15:00', 'AliciaB',    '1990-09-05', 'female',    168.20,  68.30),
  ('Marcus', 'Lee', 'marcus.lee@example.com','hash_marcus_789','2025-10-02 19:45:00','MarcusL',   '1988-01-23', 'male',      178.90,  82.10),
  ('Priya', 'Singh', 'priya.s@example.com', 'hash_priya_321', '2025-10-03 06:50:00', 'PriyaS',     '1993-07-18', 'female',    162.00,  59.80),
  ('Jordan', 'Taylor', 'jordan.t@example.com','hash_jordan_654','2025-10-03 21:10:00', 'JordT',      '1995-11-30', 'nonbinary', 175.30,  75.40),
  ('Elena', 'Martinez', 'elena.m@example.com', 'hash_elena_987', '2025-10-04 09:05:00', 'ElenaM',     '1986-02-10', 'female',    160.55,  62.20),
  ('David', 'Chen', 'david.c@example.com', 'hash_david_147', '2025-10-04 18:35:00', 'DaveC',      '1991-06-02', 'male',      181.00,  88.70),
  ('Samantha', 'Johnson', 'sam.j@example.com',   'hash_sam_258',   '2025-10-05 07:40:00', 'SamJ',       '1998-03-27', 'female',    170.10,  71.90),
  ('Omar', 'Ali', 'omar.ali@example.com','hash_omar_369',  '2025-10-05 20:20:00', 'OmarA',      '1989-08-09', 'male',      179.60,  84.30),
  ('Taylor', 'Brooks', 'taylor.b@example.com','hash_taylor_951','2025-10-06 10:25:00', 'TBrooks',    '1994-12-15', 'other',     172.75,  78.40);


/* ---------- EXERCISES (10 rows) ---------- */
INSERT INTO exercises
  (exercise_name, exercise_category, muscle_group)
VALUES
  ('Back Squat', 'strength', 'Quads & Glutes'),
  ('Bench Press', 'strength','Chest & Triceps'),
  ('Deadlift', 'strength', 'Posterior Chain'),
  ('Pull-up', 'strength',    'Back & Biceps'),
  ('Push-up', 'strength',    'Chest & Core'),
  ('Plank', 'core',        'Abdominals'),
  ('Jogging (Treadmill)', 'cardio',      'Full Body'),
  ('Cycling (Stationary)',    'cardio',      'Legs & Cardio'),
  ('Yoga Flow', 'mobility',    'Full Body'),
  ('Box Breathing Meditation','mindfulness', 'Nervous System');


/* ---------- MEALS (10 rows) ---------- */
INSERT INTO meals
  (user_id, meal_datetime, meal_type, notes)
VALUES
  (1, '2025-10-15 07:30:00', 'breakfast', 'Overnight oats with berries and hemp protein'),
  (1, '2025-10-15 13:00:00', 'lunch',     'Quinoa bowl with roasted veggies'),
  (1, '2025-10-15 19:15:00', 'dinner',    'Tofu stir-fry with brown rice'),
  (2, '2025-10-15 08:10:00', 'breakfast', 'Avocado toast and black coffee'),
  (2, '2025-10-15 12:40:00', 'lunch',     'Chickpea salad wrap'),
  (3, '2025-10-15 18:50:00', 'dinner',    'Lentil curry with basmati rice'),
  (3, '2025-10-16 10:30:00', 'snack',     'Apple with almond butter'),
  (4, '2025-10-16 07:45:00', 'breakfast', 'Tofu scramble and spinach'),
  (5, '2025-10-16 13:15:00', 'lunch',     'Grilled veggie sandwich'),
  (6, '2025-10-16 20:05:00', 'dinner',    'Black bean tacos with salsa');


/* ---------- FOOD (10 rows) ---------- */
INSERT INTO food
  (food_name, brand, serving_size_amount, serving_size_unit, calories_per_serving, protein, carbs, fat)
VALUES
  ('Overnight Oats Base',     'Homemade',  80.00,  'g',           300, 10.00, 45.00, 8.00),
  ('Mixed Berries',           'FrozenMix', 75.00,  'g',            40,  1.00, 10.00, 0.50),
  ('Hemp Protein Powder',     'Whole Foods',30.00, 'g',           120, 15.00,  7.00, 3.00),
  ('Quinoa (cooked)',         'Generic',  185.00,  'g (1 cup)',   220,  8.00, 39.00, 3.50),
  ('Roasted Veggies Mix',     'Homemade', 150.00,  'g',           110,  3.00, 18.00, 4.00),
  ('Firm Tofu',               'Nasoya',   100.00,  'g',           140, 14.00,  4.00, 8.00),
  ('Brown Rice (cooked)',     'Generic',  195.00,  'g (1 cup)',   215,  5.00, 45.00, 2.00),
  ('Chickpea Salad',          'Homemade', 150.00,  'g',           260, 12.00, 30.00, 9.00),
  ('Almond Butter',           'MaraNatha', 16.00,  'g (1 tbsp)',   98,  3.40,  3.40, 8.90),
  ('Black Bean Taco Filling', 'Homemade', 130.00,  'g',           190, 10.00, 26.00, 4.50),
  ('Spinach', 'Farm Fresh', 5.00,  'g', 10, 1.00, 1.00, 0.50);

/* ---------- MEAL_ITEMS (20 rows) ---------- */
-- Menatl note: meals 1–3 are Shaun’s full day of eating, with realistic servings
-- meals separated by user id
INSERT INTO meal_items
  (meal_id, food_id, servings)
VALUES
  -- Meal 1: Overnight oats + berries + hemp protein
  (1, 1, 1.00),
  (1, 2, 1.00),
  (1, 3, 1.00),

  -- Meal 2: Quinoa bowl with roasted veggies
  (2, 4, 1.50),
  (2, 5, 1.00),

  -- Meal 3: Tofu stir fry with brown rice
  (3, 6, 1.00),
  (3, 7, 1.00),
  (3, 5, 0.75),

  -- Meal 4: Avocado toast not in food table, approximate with chickpea salad
  (4, 8, 0.80),

  -- Meal 5: Chickpea wrap + berries
  (5, 8, 1.00),
  (5, 2, 1.00),

  -- Meal 6: Lentil curry approximated with black bean filling + rice
  (6,10, 1.00),
  (6, 7, 0.75),

  -- Meal 7: Apple + almond butter
  (7, 9, 1.50),

  -- Meal 8: Tofu scramble + veggies
  (8, 6, 0.80),
  (8, 5, 0.60),

  -- Meal 9: Veggie sandwich approximated as roasted veggies and chickpea salad
  (9, 5, 0.80),
  (9, 8, 0.70),

  -- Meal 10: Black bean tacos
  (10,10, 1.50),
  (10, 7, 0.50);

/* ---------- MOOD_ENTRIES (30 rows) ---------- */
-- Mental note: mix of users 1–5, different times and days
-- Again, i separate mood entries by users for my visual purposes.
INSERT INTO mood_entries
  (user_id, entry_datetime, mood_score, energy_level, stress_level, note)
VALUES
  (1, '2025-10-10 07:15:00', 8, 7, 3, 'Slept well, ready for the day'),
  (1, '2025-10-10 20:45:00', 6, 5, 5, 'Long work day, light workout helped'),
  (1, '2025-10-11 06:55:00', 7, 6, 4, 'CPAP fit felt better last night'),
  (1, '2025-10-11 21:10:00', 5, 4, 6, 'A bit drained, knees slightly sore'),
  (1, '2025-10-12 07:05:00', 8, 7, 3, 'Morning hoops, knee feels strong'),
  (1, '2025-10-12 21:00:00', 7, 6, 4, 'Good balance of work and recovery'),

  (2, '2025-10-10 08:30:00', 6, 5, 5, 'Rushed morning, skipped meditation'),
  (2, '2025-10-10 22:00:00', 7, 4, 3, 'Yoga class helped me unwind'),
  (2, '2025-10-11 08:10:00', 7, 6, 4, 'Solid breakfast, steady energy'),
  (2, '2025-10-11 21:40:00', 6, 5, 5, 'Screen time ran late, mind busy'),
  (2, '2025-10-12 09:00:00', 8, 7, 3, 'Walk outside felt grounding'),
  (2, '2025-10-12 21:30:00', 7, 5, 4, 'Feeling more consistent this week'),

  (3, '2025-10-09 07:00:00', 5, 4, 6, 'Did not sleep well, mind racing'),
  (3, '2025-10-09 19:45:00', 6, 5, 5, 'Evening run took edge off stress'),
  (3, '2025-10-10 07:20:00', 6, 5, 5, 'Still a bit groggy in the morning'),
  (3, '2025-10-10 20:10:00', 7, 6, 4, 'Dinner with friends boosted mood'),
  (3, '2025-10-11 07:10:00', 7, 6, 3, 'Started journaling again'),
  (3, '2025-10-11 22:00:00', 6, 4, 5, 'Late caffeine keeping me up'),

  (4, '2025-10-08 06:50:00', 8, 7, 3, 'Yoga and breathing felt amazing'),
  (4, '2025-10-08 21:20:00', 7, 5, 4, 'Mental load manageable today'),
  (4, '2025-10-09 06:45:00', 7, 6, 4, 'Slightly stiff but okay'),
  (4, '2025-10-09 20:55:00', 6, 4, 5, 'Too much context switching at work'),
  (4, '2025-10-10 06:40:00', 8, 7, 3, 'Meditation before email helped'),
  (4, '2025-10-10 21:05:00', 7, 5, 4, 'Ended day with light stretching'),

  (5, '2025-10-07 07:30:00', 6, 5, 5, 'Did not hit sleep goal'),
  (5, '2025-10-07 22:15:00', 5, 4, 6, 'Scrolling in bed too late'),
  (5, '2025-10-08 07:20:00', 7, 6, 4, 'Short meditation helped reset'),
  (5, '2025-10-08 21:45:00', 7, 5, 4, 'Screen time lower than usual'),
  (5, '2025-10-09 07:25:00', 8, 7, 3, 'Felt very focused this morning'),
  (5, '2025-10-09 21:35:00', 8, 6, 3, 'In bed by 10, proud of consistency');

/* ---------- WORKOUT_SESSIONS (12 rows) ---------- */
-- Note: primary key is 'sesion_id' per your table definition
INSERT INTO workout_sessions
  (user_id, exercise_id, session_datetime, duration_minutes, notes, sets, reps, weight)
VALUES
  (1, 7, '2025-10-10 05:45:00', 30, 'Light jog, testing knee',           NULL, NULL, NULL),
  (1, 1, '2025-10-11 06:15:00', 45, 'Back squat, focused on form',       4, 5,  80.00),
  (1, 10,'2025-10-11 06:55:00', 10, 'Box breathing cool-down',           NULL, NULL, NULL),
  (2, 9, '2025-10-10 18:00:00', 50, 'Vinyasa flow, moderate intensity',  NULL, NULL, NULL),
  (2, 6, '2025-10-11 07:30:00', 15, 'Core focus, timed planks',          3, 1,   NULL),
  (3, 8, '2025-10-09 18:30:00', 35, 'Stationary bike intervals',         NULL, NULL, NULL),
  (3, 2, '2025-10-10 17:45:00', 40, 'Bench press strength work',         5, 5,  75.00),
  (4, 9, '2025-10-08 06:00:00', 40, 'Morning yoga for mobility',         NULL, NULL, NULL),
  (4, 10,'2025-10-10 06:20:00', 8,  'Short guided breathing session',    NULL, NULL, NULL),
  (5, 7, '2025-10-07 18:10:00', 25, 'Easy treadmill jog after work',     NULL, NULL, NULL),
  (5, 3, '2025-10-09 17:30:00', 35, 'Light deadlifts, focus on hinge',   3, 5,  70.00),
  (6, 4, '2025-10-12 09:15:00', 20, 'Pull-ups EMOM, assisted',           6, 3,  NULL);


/* ---------- WEIGHT_LOGS (24 rows) ---------- */
INSERT INTO weight_logs
  (user_id, weight, weight_datetime)
VALUES
  -- User 1: Shaun (starting weight 107.50)
  (1, 107.50, '2025-10-10 07:00:00'),
  (1, 107.20, '2025-10-11 07:00:00'),
  (1, 106.90, '2025-10-12 07:00:00'),

  -- User 2: Alicia (68.30)
  (2, 68.40, '2025-10-10 08:00:00'),
  (2, 68.20, '2025-10-12 08:00:00'),

  -- User 3: Marcus (82.10)
  (3, 82.10, '2025-10-09 07:10:00'),
  (3, 81.90, '2025-10-11 07:10:00'),
  (3, 81.80, '2025-10-13 07:10:00'),

  -- User 4: Priya (59.80)
  (4, 59.90, '2025-10-08 06:50:00'),
  (4, 59.70, '2025-10-10 06:50:00'),
  (4, 59.65, '2025-10-12 06:50:00'),

  -- User 5: Jordan (75.40)
  (5, 75.40, '2025-10-07 07:20:00'),
  (5, 75.30, '2025-10-09 07:20:00'),
  (5, 75.10, '2025-10-11 07:20:00'),

  -- User 6: Elena (62.20)
  (6, 62.30, '2025-10-08 08:30:00'),
  (6, 62.10, '2025-10-11 08:30:00'),

  -- User 7: David (88.70)
  (7, 88.70, '2025-10-10 06:40:00'),
  (7, 88.40, '2025-10-12 06:40:00'),

  -- User 8: Samantha (71.90)
  (8, 72.00, '2025-10-07 07:30:00'),
  (8, 71.80, '2025-10-10 07:30:00'),

  -- User 9: Omar (84.30)
  (9, 84.30, '2025-10-09 07:50:00'),
  (9, 84.10, '2025-10-12 07:50:00'),

  -- User 10: Taylor (78.40)
  (10, 78.50, '2025-10-08 10:00:00'),
  (10, 78.30, '2025-10-11 10:00:00');



-- DATABASE ACTIONS

/*----------Views To Create---------------*/ 
/*View dailyMoodTrends: summary of the user's mood and feeds the user's mood chart*/
CREATE VIEW dailyMoodTrends AS
	SELECT
		user_id,
        DATE(entry_datetime) AS mood_date,
        ROUND(AVG(mood_score), 0) AS avg_mood_score,
        ROUND(AVG(stress_level), 0) AS avg_stress_level
	FROM
		mood_entries
	GROUP BY
		user_id, mood_date;
		
/*View workoutSummaries: summary of the user's workouts and feeds the user's workout consistency chart*/ 
CREATE VIEW workoutSummaries AS
	SELECT 
		user_id,
        DATE(session_datetime) as workout_date,
        COUNT(session_id) AS total_sessions,
        SUM(duration_minutes) AS total_duration
	FROM
		workout_sessions
	GROUP BY
		user_id, workout_date;
        
        
/*View caloriesPerDaySummaries: summary of the user's meals, calories. This feeds the users macro chart */
CREATE VIEW caloriesPerDaySummaries AS
	SELECT
		m.user_id,
		m.meal_id,
        COUNT(m.meal_id) AS total_meals,
        DATE (m.meal_datetime) as date,
        -- to get the complete calories for a food item, we have to multiply the item by the number of servings then add i all up to get total calories
        -- similar apprach for protein, carbs and fats
        ROUND(SUM((mi.servings * f.calories_per_serving)), 2) AS total_calories,
        ROUND(SUM((mi.servings * f.protein)), 2) AS total_protein,
        ROUND(SUM((mi.servings * f.carbs)), 2) AS total_carbs,
        ROUND(SUM((mi.servings * f.fat)), 2) AS total_fats
        
	FROM
		meal_items mi
	LEFT JOIN meals m ON m.meal_id = mi.meal_id
	LEFT JOIN food f ON f.food_id = mi.food_id
    GROUP BY
		m.user_id, m.meal_id, date;

			
/*View dailyWeightSummary: summary of the user's weight each day. This feeds the users weight trend chart */
CREATE VIEW dailyWeightSummary AS
	SELECT
		user_id,
        DATE(weight_datetime) as date,
        ROUND(weight, 2) AS user_weight
	FROM
		weight_logs
	GROUP BY
		user_id, date, user_weight;
        
        
/*----------Functions---------------*/ 
DROP FUNCTION IF EXISTS getUserID;
-- Changing delimiter to $$ so it runs everthing within the delimiter block as one.
DELIMITER $$

/*---------This function gets the user ID if it exists------*/
CREATE FUNCTION getUserID(myUsername VARCHAR(100))
RETURNS INT DETERMINISTIC
BEGIN
	-- Declaring the variable that will hold the output to be returned
	DECLARE foundUserID INT;
		-- Checking if users exists and loading output into  declard variable
		SELECT user_id INTO foundUserID
        FROM users
        WHERE username = myUsername;
        
        -- Logic to determine output if user exists or not
        IF foundUserID is NULL
        THEN SET foundUserID = -1;
        END IF;
        
        RETURN foundUserID;
END$$

-- Changing delimiter back to ;
DELIMITER ;

-- select getUserID('ShaunC') AS foundUserID;

DROP FUNCTION IF EXISTS getUserName;

DELIMITER $$
/*---------This function gets the username if it exists------*/
CREATE FUNCTION getUserName(myUsername VARCHAR(100))
RETURNS VARCHAR(100) DETERMINISTIC
BEGIN
	DECLARE foundUserName VARCHAR(100);
    SELECT username INTO foundUserName
    FROM users
    WHERE username = myUsername;
    
    IF foundUserName IS NULL
    THEN SET foundUserName = -1;
    END IF;
    
    RETURN foundUserName;
END$$

DELIMITER ;

-- select getUserName('ShaunC') AS foundUserName;

DROP FUNCTION IF EXISTS getUserEmail;

DELIMITER $$

/*-------This function checks if and email adreess exists------*/
CREATE FUNCTION getUserEmail(myEmail VARCHAR(100))
RETURNS  VARCHAR(150) DETERMINISTIC
BEGIN
	DECLARE foundUserEmail VARCHAR(150);
    SELECT email INTO foundUserEmail
    FROM users
    WHERE email = myEmail;
    
    IF foundUserEmail IS NULL
    THEN SET foundUserEmail = -1;
    END IF;
    
    RETURN foundUserEmail;
END$$

DELIMITER ;

-- select getUserEmail('shaun@example.com') AS foundUserEmail;

DROP FUNCTION IF EXISTS getExerciseID;

DELIMITER $$
/*---------This function gets the ExerciseID if it exists------*/
CREATE FUNCTION getExerciseID(myExerciseName VARCHAR(100))
RETURNS INT DETERMINISTIC
BEGIN
	DECLARE foundExerciseID INT;
    SELECT exercise_id INTO foundExerciseID
    FROM exercises
    WHERE exercise_name = myExerciseName;
    
    IF foundExerciseID IS NULL
    THEN SET foundExerciseID = -1;
    END IF;
    
    RETURN foundExerciseID;
END$$

DELIMITER ;

-- select getExerciseID('Back Squat') AS ExerciseID;

DROP FUNCTION IF EXISTS getFoodID;

DELIMITER $$
/*---------This function gets the food id if it exists------*/
CREATE FUNCTION getFoodID(myFoodName VARCHAR(100))
RETURNS INT DETERMINISTIC
BEGIN
	DECLARE foundFoodID INT;
    SELECT food_id INTO foundFoodID
    FROM food
    WHERE food_name = myFoodName;
    
    IF foundFoodID IS NULL
    THEN SET foundFoodID = -1;
    END IF;
    
    RETURN foundFoodID;
END$$

DELIMITER ;

-- select getFoodID('Overnight Oats Base') AS foodID;

/*----------Procedures to be created---------------*/  


DROP PROCEDURE IF EXISTS createUser;

-- Changing delimiter to $$ so it runs everthing within the delimiter block as one.
DELIMITER $$

/*-----------This procedure creates a user-----------*/
CREATE PROCEDURE createUser(
	IN ufirst_name VARCHAR(50), ulast_name VARCHAR(50), uemail VARCHAR(150),
    upassword_hash VARCHAR(255), ucreated_at DATETIME, uusername VARCHAR(100),
    udate_of_birth DATE, ugender ENUM('male','female','nonbinary','other'),
    uheight DECIMAL(5,2), uweight DECIMAL(5,2)
)

BEGIN
	-- declaring return variableS
    DECLARE foundUserName VARCHAR(100);
    DECLARE foundUserEmail VARCHAR(150);
    
    -- calling get username to handle if uename already exists and handle errors
    SELECT getUserName(uusername) INTO foundUserName;
    -- calling get user email to make sure email does not exist and handle errors
    SELECT getUserEmail(uemail) INTO foundUserEmail;
    
    -- Logic to handle if username or email already used in DB before creating user
	IF foundUserName != -1
	THEN SELECT -1 AS userNameExists;
	ELSEIF foundUserEmail != -1
	THEN SELECT -2 AS userEmailExists;
    ELSE
		-- if the user does not exist create it
		INSERT INTO users (
			first_name, last_name, email,
            password_hash, created_at, username,
            date_of_birth, gender, height, weight
        )
        VALUES (
			ufirst_name, ulast_name, uemail,
            upassword_hash, ucreated_at, uusername,
            udate_of_birth, ugender, uheight, uweight
        );
	END IF;
    
    -- return the user ID of the user that was just created, thi sshould return the ID or 0
    SELECT getUserID(uusername) AS userID;
    
-- signaling where the code block ends
END$$
    
-- setting the delimiter back to what it was
DELIMITER ;
    
-- CALL createUser('Michael', 'Jordan', 'michael@example.com', 'hash_michael_123', '2025-10-01 07:30:00',	'MichaelJ', '1983-04-12',	'male',	185.42,	107.50);


/*-----------This procedure log's the users's mood-----------*/
DROP PROCEDURE IF EXISTS logMood;

DELIMITER $$

CREATE PROCEDURE logMood(
	myUserName VARCHAR(100),
	myEntryDatetime DATETIME,
	myMoodScore TINYINT,
	myEnergyLevel TINYINT,
	myStressLevel TINYINT,
	myNote TEXT
)

BEGIN
	-- Declaring variable to hold returned user ID
	DECLARE foundUserID INT;
    -- Getting the user ID if it exists and storing in variable
    SELECT getUserID(myUserName) INTO foundUserID;
    
    -- If the user does not exist then return not found
    IF foundUserID = -1
    THEN SELECT -2 AS notFound;
    ELSE
		INSERT INTO mood_entries (
			user_id, entry_datetime,
            mood_score, energy_level,
            stress_level, note
        )
		VALUES(
			foundUserID, myEntryDatetime,
			myMoodScore, myEnergyLevel,
			myStressLevel, myNote
        );
        
		-- returning 0 if mood logged successfully
		SELECT 0 AS moodLogged;
	END IF;
    
END$$

DELIMITER ;

-- CALL logMood('MichaelJ', '2025-10-10 07:15:00', 10, 10, 6, 'Morning hoops, knee feels strong');


/*-----------This procedure log's the users's workout-----------*/
DROP PROCEDURE IF EXISTS logWorkout;

DELIMITER $$

CREATE PROCEDURE logWorkout(
	myUserName VARCHAR(100),
	myExerciseName VARCHAR(100),
	mySessionDatetime DATETIME,
	myDurationMinutes INT,
	myNotes TEXT,
	mySets INT,
	myReps INT,
	myWeight DECIMAL(6,2)
)

BEGIN
	-- Declaring variable to hold returned user ID
	DECLARE foundUserID INT;
    DECLARE foundExerciseID INT;
    
    -- Getting the user ID if it exists and storing in variable
    SELECT getUserID(myUserName) INTO foundUserID;
    -- Getting exercise ID as well
    SELECT getExerciseID(myExerciseName) INTO foundExerciseID;
    
    -- If the user or exercise does not exist then return not found
    IF foundUserID = -1 AND foundExerciseID = -1
    THEN SELECT -3 AS UserAndExerciseNotFound;
    ELSEIF foundUserID = -1
    THEN SELECT -2 AS userNotFound;
    ELSEIF foundExerciseID = -1
    THEN SELECT -1 AS exerciseNotFound;
    ELSE
		INSERT INTO workout_sessions (
			user_id, exercise_id,
            session_datetime, duration_minutes,
            notes, sets, reps, weight
        )
		VALUES(
			foundUserID, foundExerciseID,
			mySessionDatetime, myDurationMinutes,
			myNotes, mySets,
			myReps, myWeight
        );
        
		-- returning 0 if workout session logged successfully
		SELECT 0 AS workoutSessionLogged;
	END IF;
    
END$$

DELIMITER ;

-- CALL logWorkout('MichaelJ', 'Back Squat', '2025-10-10 05:45:00', 90, 'Back squat, focused on form', 4, 5,  80.00);


/*-----------This procedure log's the users's meal-----------*/
DROP PROCEDURE IF EXISTS addMeal;

DELIMITER $$

CREATE PROCEDURE addMeal(
	myUserName VARCHAR(100), mymealDatetime DATETIME,
    myMealTypes ENUM('breakfast','lunch','dinner','snack'), myNotes TEXT,
    OUT mymealID INT
)

BEGIN
	-- Declaring variable to hold returned user ID
	DECLARE foundUserID INT;
    
    SELECT getUserID(myUserName) INTO foundUserID;
  
    -- If the user ID does not exist then return not found
    IF foundUserID = -1 
    THEN SELECT -1 AS foundUserID;
    ELSE
		INSERT INTO meals (
			user_id, meal_datetime, meal_type, notes
        )
		VALUES(
			foundUserID, mymealDatetime, myMealTypes, myNotes
        );
        
		-- Getting the ID for the meal that was just created
		SET myMealID = LAST_INSERT_ID();
        
        -- returning 0 if item logged successfully
		SELECT 0 AS mealItemLogged;

	END IF;
    
END$$

DELIMITER ;


/*-----------This procedure log's the users's meal items-----------*/
DROP PROCEDURE IF EXISTS addMealItem;

DELIMITER $$

CREATE PROCEDURE addMealItem(
	myMealID INT, myFoodName VARCHAR(100), myServings DECIMAL(5,2)
)

BEGIN
	DECLARE foundFoodID INT;
    
    SELECT getFoodID(myFoodName) INTO foundFoodID;
  
    -- If the Meal ID does not exist then return not found
    IF myMealID IS NULL AND foundFoodID = -1
    THEN SELECT -3 AS mealfoodNotFound;
    ELSEIF myMealID IS NULL
    THEN SELECT -2 AS mealIDNotFound;
    ELSEIF foundFoodID = -1
    THEN SELECT -1 AS foodIDNotFound;
    ELSE
		INSERT INTO meal_items (
			meal_id, food_id, servings
        )
		VALUES(
			myMealID, foundFoodID, myServings
        );
        
		-- returning 0 if meal item logged successfully
		SELECT 0 AS mealLogged;
	END IF;
    
END$$

DELIMITER ;

-- Creating an empty variable to hold the meal ID output from the addmeal procedure
SET @meal_id = NULL;

-- Calling create meal procedure
CALL addMeal('MichaelJ', '2025-10-15 13:00:00', 'lunch', 'Tofu scramble and spinach', @meal_id);

select @meal_id as mealID;

-- Calling addMealItem procedure

-- CALL addMealItem(@meal_id, 'Firm Tofu', 4);


/*-----------This procedure log's the users's weight-----------*/
DROP PROCEDURE IF EXISTS logWeight;

DELIMITER $$

CREATE PROCEDURE logWeight(
	myUserName VARCHAR(100),
	myWeight DECIMAL(5,2),
	myWeightDatetime DATETIME
)

BEGIN
	-- Declaring variable to hold returned user ID
	DECLARE foundUserID INT;
    
    SELECT getUserID(myUserName) INTO foundUserID;
  
    -- If the user ID does not exist then return not found
    IF foundUserID = -1 
    THEN SELECT -1 AS foundUserID;
    ELSE
		INSERT INTO weight_logs (
			user_id, weight, weight_datetime
        )
		VALUES(
			foundUserID, myWeight, myWeightDatetime
        );
        
        -- returning 0 if item logged successfully
		SELECT 0 AS weightLogged;

	END IF;
    
END$$

DELIMITER ;

-- CALL logWeight('MichaelJ', 107.20, '2025-10-11 07:00:00');


/*-----------This procedure update's the users's password-----------*/
DROP PROCEDURE IF EXISTS resetPassword;

DELIMITER $$

CREATE PROCEDURE resetPassword(
	myNewPassowrd VARCHAR(255),
	myUserName VARCHAR(100),
	myEmail VARCHAR(150)
)

BEGIN
	-- Declaring variable to hold returned user ID and Email ID
	DECLARE foundUserID INT;
    DECLARE foundEmail VARCHAR(150);
    DECLARE emailLookUp VARCHAR(150);
    
    SELECT getUserID(myUserName) INTO foundUserID;
    SELECT getUserEmail(myEmail) INTO foundEmail;
    
    -- Making sure username and email match
    SELECT email
		FROM users
		WHERE user_id = foundUserID
        INTO emailLookUp;
        
    -- If the user ID does not exist then return -1 not found
    IF emailLookUp != foundEmail
    THEN SELECT -3 AS emailNotound;
    -- ELSEIF foundUserID = -1 AND foundEmail = -1
   -- THEN SELECT -2 AS userEmailIDnotFound;
   -- ELSEIF foundUserID = -1
   -- THEN SELECT -1 AS userNotFound;
    ELSE
		UPDATE users
        SET password_hash = myNewPassowrd
        WHERE user_id = foundUserID AND email = foundEmail;
		
        -- returning 0 if item updated successfully
		SELECT 0 AS passwordUpdated;

	END IF;
    
END$$

DELIMITER ;

-- CALL resetPassword('hash_michael_2333', 'MichaelJ', 'michael@example.com');

/*-----------This procedure delete's the users's account-----------*/
DROP PROCEDURE IF EXISTS deleteAccount;

DELIMITER $$

CREATE PROCEDURE deleteAccount(
	myUserName VARCHAR(100)
)

BEGIN
	-- Declaring variable to hold returned user ID
	DECLARE foundUserID INT;
    
    
    -- Getting the user ID if it exists and storing in variable
    SELECT getUserID(myUserName) INTO foundUserID;
    
    IF foundUserID = -1
    THEN SELECT -1 AS userNotFound;
    ELSE
		-- Deleting user account
		DELETE FROM users
		WHERE user_id = foundUserID;
	
        -- returning 0 if item deleted successfully
		SELECT 0 AS accountDeleted;

	END IF;
    
END$$

DELIMITER ;

-- CALL deleteAccount('ShaunC'); 
    
/*Notes for me
Procedures to create
logMood*******Done
logWorkout********Done
createMeal*******Done
addMealItem*******Done
logWeight*******Done
update password *** Done
delete account *** Done

*/




-- USE `mbd`;

-- select *  FROM users;

-- SELECT *
-- FROM mood_entries;

-- SELECT *
-- FROM meals;

-- SELECT *
-- FROM meal_items;

-- SELECT *
-- FROM food;

-- SELECT *
-- FROM workout_sessions;

-- SELECT *
-- FROM exercises;

-- SELECT *
-- FROM weight_logs;

-- select * FROM dailyMoodTrends;

-- select * from workoutSummaries;

-- select * from caloriesPerDaySummaries;

-- select * from dailyWeightSummary;





