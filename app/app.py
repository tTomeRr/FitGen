from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import psycopg2
from sqlalchemy import text, create_engine

load_dotenv()  # This loads the variables from .env file

app = Flask(__name__)
db_uri = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@localhost/flex"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

@app.route('/test_db_connection')
def test_db_connection():
    try:
        # Create an engine and connect to it for testing
        engine = create_engine(db_uri)
        with engine.connect() as connection:
            result = connection.execute(text('SELECT 1'))
            return 'Connected to the database.'
    except Exception as e:
        return 'Failed to connect to the database: ' + str(e)

class Workout(db.Model):
    __tablename__ = 'workouts'
    workout_id = db.Column(db.Integer, primary_key=True)
    workout_name = db.Column(db.String)
    workout_duration = db.Column(db.String)
    fitness_level = db.Column(db.String)
    fitness_goal = db.Column(db.String)
    equipment_access = db.Column(db.String)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['Message']

        print(name, email, phone, message)

    return render_template('index.html')


@app.route('/workout')
def workout():
    return render_template('workout.html')


@app.route('/workout/run', methods=['GET', 'POST'])
def run():
    if request.method == 'POST':
        duration = request.form['workout-duration']
        level = request.form['fitness-level']
        run_type = request.form['running-type']

        # Do something with the data
        print(duration, level, run_type)

    return render_template('run.html')


@app.route('/workout/strength', methods=['GET', 'POST'])
def strength():
    if request.method == 'POST':
        duration = request.form['workout-duration']
        level = request.form['fitness-level']
        goal = request.form['fitness-goal']
        equipment = request.form['equipment-access']
        print(duration, level, goal, equipment)

    return render_template('strength.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404


@app.route('/workouts')
def get_workouts():
    try:
        workouts = Workout.query.filter(
            Workout.workout_duration == '0-30',
            Workout.fitness_level == 'beginner',
            Workout.fitness_goal == 'lose-fat',
            Workout.equipment_access == 'home'
        ).all()
        return jsonify([{'workout_id': w.workout_id, 'workout_name': w.workout_name} for w in workouts])
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == "__main__":
    app.run()
