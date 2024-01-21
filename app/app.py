from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import random
import datetime
from sqlalchemy import text, create_engine

load_dotenv()  # This loads the variables from .env file

app = Flask(__name__)
db_uri = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@localhost/flex"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)


class Workout(db.Model):
    __tablename__ = 'workouts'
    workout_id = db.Column(db.Integer, primary_key=True)
    workout_name = db.Column(db.String)
    workout_type = db.Column(db.String)
    workout_duration = db.Column(db.String)
    fitness_level = db.Column(db.String)
    fitness_goal = db.Column(db.String)
    equipment_access = db.Column(db.String)
    running_type = db.Column(db.String)


class Exercises(db.Model):
    __tablename__ = 'exercises'
    exercise_id = db.Column(db.Integer, primary_key=True)
    exercise_name = db.Column(db.String)
    exercise_type = db.Column(db.String)
    exercise_description = db.Column(db.String)


class WorkoutExercises(db.Model):
    __tablename__ = 'workoutexercises'
    workout_id = db.Column(db.Integer, db.ForeignKey('Workouts.workout_id'), primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('Exercises.exercise_id'), primary_key=True)
    sets = db.Column(db.Integer)
    repetitions = db.Column(db.String(20))
    rest_time = db.Column(db.String(20))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['Message']

        print(name, email, phone, message)

    year = datetime.date.today().year
    return render_template('index.html', year=year)


@app.route('/workout')
def workout():
    return render_template('workout.html')


@app.route('/workout/run', methods=['GET', 'POST'])
def run():
    if request.method == 'POST':
        duration = request.form['workout-duration']
        level = request.form['fitness-level']
        running_type = request.form['running-type']
        print(duration, level, running_type)
        return redirect(url_for('get_run_workouts', duration=duration, fitness_level=level, running_type=running_type))

    return render_template('run.html')


@app.route('/workout/strength', methods=['GET', 'POST'])
def strength():
    if request.method == 'POST':
        duration = request.form['workout-duration']
        level = request.form['fitness-level']
        goal = request.form['fitness-goal']
        equipment = request.form['equipment-access']
        print(duration, level, goal, equipment)
        return redirect(url_for('get_strength_workouts', duration=duration, fitness_level=level, fitness_goal=goal,
                                equipment_access=equipment))

    return render_template('strength.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404


@app.route('/strength_workouts')
def get_strength_workouts():
    duration = request.args.get('duration')
    fitness_level = request.args.get('fitness_level')
    fitness_goal = request.args.get('fitness_goal')
    equipment_access = request.args.get('equipment_access')

    workouts = Workout.query.filter(
        Workout.workout_duration == duration,
        Workout.fitness_level == fitness_level,
        Workout.fitness_goal == fitness_goal,
        Workout.equipment_access == equipment_access
    ).all()

    if len(workouts) != 0:
        workout_ids = [workout.workout_id for workout in workouts]
        selected_workout_id = random.choice(workout_ids)
        return redirect(url_for('display_workout', workout_id=selected_workout_id))
    else:
        return redirect(
            url_for('ai_workout', duration=duration, fitness_level=fitness_level, fitness_goal=fitness_goal,
                    equipment_access=equipment_access))



@app.route('/display-workout/<int:workout_id>')
def display_workout(workout_id):
    workout_details = db.session.query(
        Exercises.exercise_name,
        Exercises.exercise_description,
        WorkoutExercises.sets,
        WorkoutExercises.repetitions,
        WorkoutExercises.rest_time
    ).join(WorkoutExercises, WorkoutExercises.exercise_id == Exercises.exercise_id) \
     .join(Workout, Workout.workout_id == WorkoutExercises.workout_id) \
     .filter(Workout.workout_id == workout_id) \
     .all()

    workout = Workout.query.with_entities(Workout.workout_name).filter(Workout.workout_id == workout_id).first()
    workout_name = workout.workout_name
    return render_template('workouts.html', workout_name=workout_name, exercises=workout_details)





@app.route('/get_ai_workouts', methods=['GET', 'POST'])
def ai_workout():

    duration = request.args.get('duration')
    fitness_level = request.args.get('fitness_level')
    fitness_goal = request.args.get('fitness_goal')
    equipment_access = request.args.get('equipment_access')

    return render_template('no-workouts.html')


@app.route('/run_workouts')
def get_run_workouts():
    duration = request.args.get('duration')
    fitness_level = request.args.get('fitness_level')
    running_type = request.args.get('running_type')
    print(duration, fitness_level, running_type)

    workouts = Workout.query.filter(
        Workout.workout_duration == duration,
        Workout.fitness_level == fitness_level,
        Workout.running_type == running_type
    ).all()

    if len(workouts) != 0:
        workout_ids = [workout.workout_id for workout in workouts]
        selected_workout_id = random.choice(workout_ids)
        return redirect(url_for('display_workout', workout_id=selected_workout_id))
    else:
        return redirect(
            url_for('ai_workout', duration=duration, fitness_level=fitness_level, running_type=running_type))


if __name__ == "__main__":
    app.run()
