from flask import render_template, request, redirect, url_for, session, Blueprint
import random
import datetime
from .utils import send_mail, generate_ai_workout
from .models import Workout, Exercises, WorkoutExercises, db

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['Message']
        send_mail(name, email, phone, message)

    year = datetime.date.today().year
    return render_template('index.html', year=year)


@main.route('/workout')
def workout():
    return render_template('workout.html')


@main.route('/workout/run', methods=['GET', 'POST'])
def run():
    if request.method == 'POST':
        duration = request.form['workout-duration']
        level = request.form['fitness-level']
        running_type = request.form['running-type']
        print(duration, level, running_type)
        return redirect(
            url_for('main.get_run_workouts', duration=duration, fitness_level=level, running_type=running_type))

    return render_template('run.html')


@main.route('/workout/strength', methods=['GET', 'POST'])
def strength():
    if request.method == 'POST':
        duration = request.form['workout-duration']
        level = request.form['fitness-level']
        goal = request.form['fitness-goal']
        equipment = request.form['equipment-access']
        print(duration, level, goal, equipment)
        return redirect(url_for('main.get_strength_workouts', duration=duration, fitness_level=level, fitness_goal=goal,
                                equipment_access=equipment))

    return render_template('strength.html')


@main.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404


@main.route('/strength_workouts')
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
        return redirect(url_for('main.display_workout', workout_id=selected_workout_id))
    else:
        return redirect(
            url_for('main.ai_workout', duration=duration, fitness_level=fitness_level, fitness_goal=fitness_goal,
                    equipment_access=equipment_access))


@main.route('/display-workout/<int:workout_id>')
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
    print(workout_details)
    workout = Workout.query.with_entities(Workout.workout_name).filter(Workout.workout_id == workout_id).first()
    workout_name = workout.workout_name
    print(type(workout_details))
    return render_template('workouts.html', workout_name=workout_name, exercises=workout_details)


@main.route('/get_ai_workouts', methods=['GET', 'POST'])
def ai_workout():
    if request.method == 'POST':
        # Use request.form for POST request
        duration = request.form.get('duration')
        fitness_level = request.form.get('fitness_level')
        fitness_goal = request.form.get('fitness_goal')
        equipment_access = request.form.get('equipment_access')
        running_type = request.form.get('running_type')
    else:
        # Use request.args for GET request
        duration = request.args.get('duration')
        fitness_level = request.args.get('fitness_level')
        fitness_goal = request.args.get('fitness_goal')
        equipment_access = request.args.get('equipment_access')
        running_type = request.args.get('running_type')

    if request.method == 'POST':

        workout_output = generate_ai_workout(duration, fitness_level, fitness_goal, equipment_access, running_type)

        try:
            session['workout_name'] = workout_output["workout_name"]
            session['workout_details'] = workout_output["workout_details"]
            return redirect(url_for('main.display_ai_workout'))

        except ValueError as e:
            print("Error parsing the output:", e)
            # Handle the error, maybe return an error message to the user

    return render_template('no-workouts.html')


@main.route('/run_workouts')
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
        return redirect(url_for('main.display_workout', workout_id=selected_workout_id))
    else:
        return redirect(
            url_for('main.ai_workout', duration=duration, fitness_level=fitness_level, running_type=running_type))


@main.route('/display-ai-workout')
def display_ai_workout():
    workout_name = session.get('workout_name', 'Default Workout')
    workout_details_tuples = session.get('workout_details', [])
    workout_details = [
        {'exercise_name': detail[0], 'exercise_description': detail[1],
         'sets': detail[2], 'repetitions': detail[3], 'rest_time': detail[4]}
        for detail in workout_details_tuples
    ]
    return render_template('workouts.html', workout_name=workout_name, exercises=workout_details)
