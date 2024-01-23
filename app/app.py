from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import random
import datetime
import smtplib
import ast
from openai import OpenAI


load_dotenv()  # This loads the variables from .env file

app = Flask(__name__)
app.secret_key = "Sachin"
db_uri = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@localhost:5433/flex"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)


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
        send_mail(name, email, phone, message)

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
    print(workout_details)
    workout = Workout.query.with_entities(Workout.workout_name).filter(Workout.workout_id == workout_id).first()
    workout_name = workout.workout_name
    print(type(workout_details))
    return render_template('workouts.html', workout_name=workout_name, exercises=workout_details)


@app.route('/get_ai_workouts', methods=['GET', 'POST'])
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
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"Create a workout plan with only the workout name and details based on these criteria:\n"
                        f"- Workout Duration: '{duration} minutes'\n- Fitness Level: '{fitness_level}'\n- "
                        f"Fitness Goal: '{fitness_goal}'\n- Equipment Access: '{equipment_access}'\n- Running Type: '{running_type}'\n\n"
                        "Format:\n{\n  'workout_name': 'Name of the workout',\n  "
                        "'workout_details': [('Exercise Name', 'Description', Sets, Repetitions, 'Rest Time in minutes'), ...]\n}\n"
                        "Note: Provide the response in this exact format, without any additional text.\n"
                        "Provide a workout name that reflects the workout's focus and goal, e.g., 'Intense Cardio Circuit' or 'Beginners Full-Body Strength. with no punctuation marks"
                    )
                }
            ]
        )

        output = completion.choices[0].message.content
        output = output.replace("'", '"')
        workout_dict = ast.literal_eval(output)
        session['workout_name'] = workout_dict["workout_name"]
        session['workout_details'] = workout_dict["workout_details"]
        return redirect(url_for('display_ai_workout'))

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


def send_mail(name, email, phone, message):
    gmail_user = os.getenv('GMAIL_USERNAME')
    gmail_password = os.getenv('GMAIL_PASSWORD')

    sent_from = gmail_user
    to = [gmail_user]
    subject = f'Message from: Name- {name} Email- {email}, Phone- {phone}'
    body = message

    email_text = f"""From: {sent_from}\nTo: {", ".join(to)}\nSubject: {subject}\n\n{body}"""

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        flash("Thanks for reaching us. Your message has been sent!")


    except Exception as e:
        flash(f'Something went wrong')
        print(e)

    return redirect(url_for('index'))

@app.route('/display-ai-workout')
def display_ai_workout():
    workout_name = session.get('workout_name', 'Default Workout')
    workout_details_tuples = session.get('workout_details', [])
    workout_details = [
        {'exercise_name': detail[0], 'exercise_description': detail[1],
         'sets': detail[2], 'repetitions': detail[3], 'rest_time': detail[4]}
        for detail in workout_details_tuples
    ]
    return render_template('workouts.html', workout_name=workout_name, exercises=workout_details)




if __name__ == "__main__":
    app.run()