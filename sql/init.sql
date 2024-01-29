CREATE TABLE workouts (
  workout_id SERIAL PRIMARY KEY,
  workout_name VARCHAR(50),
  workout_type VARCHAR(50),
  workout_duration VARCHAR(10),
  fitness_level VARCHAR(20),
  fitness_goal VARCHAR(50),
  equipment_access VARCHAR(50),
  running_type VARCHAR(20)
);

CREATE TABLE exercises (
  exercise_id SERIAL PRIMARY KEY,
  exercise_name VARCHAR(50),
  exercise_type VARCHAR(50),
  exercise_description VARCHAR(100)
);

CREATE TABLE workoutexercises (
  workout_id INT,
  exercise_id INT,
  sets INT,
  repetitions VARCHAR(20),
  rest_time VARCHAR(20),
  FOREIGN KEY (Workout_id) REFERENCES Workouts(workout_id),
  FOREIGN KEY (Exercise_id) REFERENCES Exercises(exercise_id)
);

INSERT INTO Workouts  (workout_name, workout_type, workout_duration, fitness_level, fitness_goal, equipment_access, running_type) VALUES
    ('Full Body Workout', 'strength', '30-60', 'intermediate', 'muscle', 'gym', NULL),
    ('Upper Body Focus', 'strength', '30-60', 'beginner', 'get-lean', 'gym', NULL),
    ('Legs and Core Strength', 'strength', '30-60', 'advanced', 'strength', 'gym', NULL),
    ('Basic Bodyweight Routine', 'strength', '0-30', 'beginner', 'lose-fat', 'home', NULL),
    ('Intermediate Calisthenics', 'strength', '60+', 'intermediate', 'get-lean', 'home', NULL),
    ('Advanced Bodyweight Challenge', 'strength', '30-60', 'advanced', 'strength', 'home', NULL),
    ('Interval Training', 'run', '30-60', 'beginner', NULL, NULL, 'hiit'),
    ('Distance Running', 'run', '60+', 'intermediate', NULL, NULL, 'long-run'),
    ('Hill Repeats', 'run', '30-60', 'advanced', NULL, NULL, 'hiit'),
    ('Easy Short Run', 'run', '0-30', 'advanced', NULL, NULL, 'hiit'),
    ('Core and Back Power', 'strength', '60+', 'intermediate', 'muscle', 'gym', NULL),
    ('Full Body Circuit', 'strength', '30-60', 'advanced', 'strength', 'gym', NULL),
    ('Home Cardio Strength', 'strength', '0-30', 'beginner', 'lose-fat', 'home', NULL),
    ('Upper Body Blast', 'strength', '30-60', 'intermediate', 'get-lean', 'home', NULL),
    ('Speed Endurance Run', 'run', '30-60', 'intermediate', NULL, NULL, 'hiit'),
    ('Recovery Easy Jog', 'run', '30-60', 'beginner', NULL, NULL, 'recovery'),
    ('Quick Recovery Run', 'run', '0-30', 'beginner', NULL, NULL, 'recovery'),
    ('Express Full Body', 'strength', '0-30', 'intermediate', 'muscle', 'gym', NULL),
    ('Quick Upper Body', 'strength', '0-30', 'beginner', 'get-lean', 'gym', NULL),
    ('Quick Bodyweight Circuit', 'strength', '0-30', 'intermediate', 'lose-fat', 'home', NULL),
    ('Gym Lower Body Blast', 'strength', '30-60', 'intermediate', 'muscle', 'gym', NULL),
    ('Upper Body & Core Gym', 'strength', '30-60', 'advanced', 'strength', 'gym', NULL),
    ('Bodyweight Cardio Mix', 'strength', '0-30', 'beginner', 'lose-fat', 'home', NULL),
    ('Intense Full Body Home', 'strength', '30-60', 'intermediate', 'get-lean', 'home', NULL);

INSERT INTO Exercises (exercise_name, exercise_type, exercise_description)
VALUES
  ('Rest', 'Active Recovery', 'Take a break and recover'), 
  ('Squats', 'Strength', 'Lower into squat position'), 
  ('Lunges', 'Strength', 'Step forward and lower into lunge'), 
  ('Plank', 'Strength', 'Hold body straight as a plank'), 
  ('Push-ups', 'Strength', 'Lower and raise chest off the floor'), 
  ('Pull-ups', 'Strength', 'Grab bar with palms facing away and pull body up'), 
  ('Chin-ups', 'Strength','Grab bar with palms facing you and pull body up'), 
  ('Dips', 'Strength', 'Lower and raise body between parallel bars'), 
  ('Burpees', 'Cardio', 'Squat down, kick feet back, do a push-up, jump up'), 
  ('Dead-lifts', 'Strength', 'Lift a weighted barbell off the floor'), 
  ('Bench Press', 'Strength', 'Lie on a bench and press a weighted barbell upwards'), 
  ('Overhead Press', 'Strength', 'Press a weighted barbell overhead'), 
  ('Bicep Curls', 'Strength', 'Curl dumbbells up to work biceps'), 
  ('Calf Raises', 'Strength', 'Raise up onto toes to work calves'), 
  ('Sprints', 'Cardio', 'Run short distances as fast as possible'), 
  ('Jogging', 'Cardio', 'Run at a steady, moderate pace'), 
  ('Hill Sprints', 'Cardio', 'Sprint up a hill then jog or walk back down'), 
  ('Walking', 'Cardio', 'Walk at a brisk steady pace'),
  ('Tricep Kickbacks', 'Strength', 'Bend forward slightly, extend arms behind'),
  ('Mountain Climbers', 'Cardio', 'Start in plank, alternate bringing knees to chest'),
  ('Russian Twists', 'Strength', 'Sit and twist torso with or without weight'),
  ('Box Jumps', 'Cardio', 'Jump onto and off a sturdy box or platform'),
  ('Leg Press', 'Strength', 'Press weight away using leg strength');


INSERT INTO WorkoutExercises (workout_id, exercise_id, sets, repetitions, rest_time)
VALUES
  (1, 2, 3, 10, 1.5),
  (1, 4, 3, 30, 1),
  (1, 5, 3, 12, 1.5),
  (1, 6, 3, 8, 2),
  (1, 9, 3, 15, 1),
  (1, 11, 3, 10, 2),
  (2, 9, 1, 30, 3),
  (2, 13, 3, 10, 1.5),
  (2, 10, 3, 6, 1.5),
  (2, 12, 2, 8, 1.5),
  (2, 10, 3, 6, 1.5),
  (2, 6, 4, 5, 3),
  (3, 2, 4, 12, 2),
  (3, 3, 4, 10, 1.5),
  (3, 4, 3, 40, 1),
  (3, 9, 3, 15, 1.5),
  (3, 14, 4, 15, 1.5),
  (4, 4, 4, 30, 1),
  (4, 5, 3, 15, 1.5),
  (4, 3, 3, 12, 1),
  (4, 8, 3, 10, 2),
  (5, 5, 4, 15, 1.5),
  (5, 6, 3, 8, 2),
  (5, 8, 3, 10, 1.5),
  (5, 3, 3, 12, 1),
  (5, 4, 3, 45, 1),
  (6, 7, 4, 8, 2),
  (6, 9, 4, 20, 1),
  (6, 12, 3, 10, 1.5),
  (6, 2, 4, 15, 1.5),
  (6, 14, 4, 20, 1),
  (7, 15, 10, '30 sec', 1),
  (7, 17, 5, '1 min', 1.5),
  (8, 16, 1, '65 min', 0),
  (9, 17, 8, '2 min', 2),
  (10, 16, 1, '20-30 min', 0),
  (11, 5, 5, 12, '1.5 min'),
  (11, 7, 5, 10, '2 min'),
  (11, 12, 5, 10, '1.5 min'),
  (11, 14, 5, 15, '1 min'),
  (12, 2, 3, 10, '1.5 min'),
  (12, 3, 3, 12, '1 min'),
  (12, 6, 3, 8, '2 min'),
  (12, 10, 3, 6, '1.5 min'),
  (13, 4, 4, 30, '1 min'),
  (13, 9, 3, 20, '1 min'),
  (13, 5, 4, 15, '1.5 min'),
  (13, 3, 3, 12, '1 min'),
  (14, 7, 4, 8, '2 min'),
  (14, 5, 3, 15, '1.5 min'),
  (14, 8, 3, 10, '2 min'),
  (14, 13, 3, 12, '1.5 min'),
  (15, 15, 8, '1 min', '2 min'),
  (15, 16, 1, '45-60 min', '0'),
  (16, 16, 1, '30-45 min', '0'),
  (17, 16, 1, '20-30 min', '0'),
  (18, 2, 3, 10, '1 min'),
  (18, 11, 3, 8, '1.5 min'),
  (18, 12, 2, 10, '1 min'),
  (19, 5, 3, 12, '1 min'),
  (19, 13, 3, 12, '1 min'),
  (19, 6, 3, 8, '1.5 min'),
  (20, 4, 4, 30, '1 min'),
  (20, 5, 3, 15, '1 min'),
  (20, 9, 3, 15, '1 min'),
  (21, 10, 3, 8, '1.5 min'),
  (21, 14, 3, 15, '1 min'),
  (21, 20, 3, 10, '2 min'),
  (22, 7, 4, 10, '2 min'),
  (22, 11, 3, 8, '1.5 min'),
  (22, 18, 3, 15, '1 min'),
  (23, 17, 3, '1 min', '1 min'),
  (23, 19, 4, 20, '1 min'),
  (23, 9, 3, 15, '1 min'),
  (24, 5, 4, 12, '1.5 min'),
  (24, 18, 3, 15, '1 min'),
  (24, 19, 3, 20, '1 min');


/* Sample query to receive the workout_id and workout_name based on parameters */
/*
SELECT (workout_id, workout_name) FROM Workouts
  WHERE workout_duration = '0-30' 
  AND fitness_level = 'beginner' 
  AND fitness_goal = 'lose-fat' 
  AND equipment_access = 'home';
*/


/* Sample query to receive the workout exercises based on parameters */
/*
SELECT (exercise_name, Exercises.exercise_description, sets, repetitions, rest_time)
FROM (
  SELECT *
  FROM Workouts
  WHERE workout_duration = '0-30' 
  AND fitness_level = 'beginner' 
  AND fitness_goal = 'lose-fat' 
  AND equipment_access = 'home'
) AS filtered_workout

JOIN WorkoutExercises ON filtered_workout.workout_id = WorkoutExercises.workout_id
JOIN Exercises ON WorkoutExercises.exercise_id = Exercises.exercise_id;
*/


/* Sample query to receive the number of workouts */
/*
SELECT COUNT(*) FROM workouts;
*/


/* Sample query to receive a workout based on workout id */
/*
SELECT exercise_name, Exercises.exercise_description, sets, repetitions, rest_time
FROM Workouts
JOIN WorkoutExercises ON Workouts.workout_id = WorkoutExercises.workout_id
JOIN Exercises ON WorkoutExercises.exercise_id = Exercises.exercise_id
WHERE Workouts.workout_id = 4;
*/
