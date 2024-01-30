"""
This module defines the routing and view logic for the Flask application. It handles
requests, processes them, and returns appropriate responses, rendering HTML templates
or redirecting to other endpoints as needed.
"""

import datetime
from flask import render_template, request, redirect, url_for, session, Blueprint
from .utils import (
    send_mail,
    generate_ai_workout,
    get_number_of_workouts,
    get_number_of_exercises,
    get_workout_from_db,
    get_workout_id,
    get_workout_by_id,
)

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    """
      Renders the main page and handles form submissions for user messages.
      Sends an email with user message if the request method is POST.
      Also fetches counts for exercises and workouts to display on the main page.
    """
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['Message']
        send_mail(name, email, phone, message)

    year = datetime.date.today().year
    exercises_count = get_number_of_exercises()
    workouts_count = get_number_of_workouts()
    print(workouts_count)

    return render_template('index.html', year=year, exercises_count=exercises_count, workouts_count=workouts_count)


@main.route('/workout')
def workout():
    """Renders the workout page."""
    return render_template('workout.html')


@main.route('/workout/run', methods=['GET', 'POST'])
def run():
    """Renders the run workout page and handles the user's workout details"""
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
    """Renders the strength workout page and handles the user's workout details"""
    if request.method == 'POST':
        duration = request.form['workout-duration']
        level = request.form['fitness-level']
        goal = request.form['fitness-goal']
        equipment = request.form['equipment-access']
        print(duration, level, goal, equipment)
        return redirect(url_for('main.get_strength_workouts', duration=duration, fitness_level=level, fitness_goal=goal,
                                equipment_access=equipment))

    return render_template('strength.html')


@main.route('/strength_workouts')
def get_strength_workouts():
    """Retrieves and displays strength workouts based on user-provided criteria"""
    workout_type = "strength"
    duration = request.args.get('duration')
    fitness_level = request.args.get('fitness_level')
    fitness_goal = request.args.get('fitness_goal')
    equipment_access = request.args.get('equipment_access')

    workouts = get_workout_from_db(workout_type=workout_type, duration=duration, fitness_level=fitness_level,
                                   fitness_goal=fitness_goal, equipment_access=equipment_access)

    if len(workouts) != 0:
        workout_id = get_workout_id(workouts)
        return redirect(url_for('main.display_workout', workout_id=workout_id))

    return redirect(
        url_for('main.ai_workout', duration=duration, fitness_level=fitness_level, fitness_goal=fitness_goal,
                equipment_access=equipment_access))


@main.route('/run_workouts')
def get_run_workouts():
    """Retrieves and displays run workouts based on user-provided criteria"""
    workout_type = "run"
    duration = request.args.get('duration')
    fitness_level = request.args.get('fitness_level')
    running_type = request.args.get('running_type')

    print("run workouts: ", workout_type, duration, fitness_level, running_type)

    workouts = get_workout_from_db(workout_type=workout_type, duration=duration,
                                   fitness_level=fitness_level, running_type=running_type)

    if len(workouts) != 0:
        workout_id = get_workout_id(workouts)
        return redirect(url_for('main.display_workout', workout_id=workout_id))

    return redirect(
        url_for('main.ai_workout', duration=duration, fitness_level=fitness_level, running_type=running_type))


@main.route('/display-workout/<int:workout_id>')
def display_workout(workout_id):
    """Displays details of a specific workout."""
    workout_details = get_workout_by_id(workout_id)

    workout_name = workout_details[0].workout_name

    return render_template('workouts.html', workout_name=workout_name, exercises=workout_details)


@main.route('/get_ai_workouts', methods=['GET', 'POST'])
def ai_workout():
    """Fetch workout details and generates a workout based on user-provided criteria via AI"""
    if request.method == 'POST':
        duration = request.form.get('duration')
        fitness_level = request.form.get('fitness_level')
        fitness_goal = request.form.get('fitness_goal')
        equipment_access = request.form.get('equipment_access')
        running_type = request.form.get('running_type')

    else:
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

    return render_template('no-workouts.html')


@main.route('/display-ai-workout')
def display_ai_workout():
    """Displays details of a specific AI workout."""
    workout_name = session.get('workout_name', 'Default Workout')
    workout_details_tuples = session.get('workout_details', [])
    workout_details = [
        {'exercise_name': detail[0], 'exercise_description': detail[1],
         'sets': detail[2], 'repetitions': detail[3], 'rest_time': detail[4]}
        for detail in workout_details_tuples
    ]
    return render_template('workouts.html', workout_name=workout_name, exercises=workout_details)


@main.errorhandler(404)
def page_not_found(_):
    """Renders a custom 404 error page."""
    error_code = 404
    error_message = "We can't find the page you're looking for."
    return render_template('error.html', error_code=error_code, error_message=error_message), 404


@main.errorhandler(500)
def service_unavailable(_):
    """Renders a custom 500 error page."""
    error_code = 500
    error_message = "Internal Server error - It's not you, it's us"
    return render_template('error.html', error_code=error_code, error_message=error_message), 500
