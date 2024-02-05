"""
This module contains utility functions for sending emails, interacting with an AI to generate workouts,
querying the database for workout and exercise information, and other miscellaneous functionalities
needed across the Flask application.
"""

import os
import ast
import random
import smtplib
from flask import flash
from openai import OpenAI
from .models import Workout, Exercises, WorkoutExercises, db


def send_mail(name, email, phone, message):
    """Sends an email using the specified Gmail credentials."""

    gmail_user = os.getenv('GMAIL_USERNAME')
    gmail_password = os.getenv('GMAIL_PASSWORD')

    sent_from = gmail_user
    to = [gmail_user]
    subject = f'Message from: Name- {name} Email- {email}, Phone- {phone}'

    email_text = f"""From: {sent_from}\nTo: {", ".join(to)}\nSubject: {subject}\n\n{message}"""

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()
        flash("Thanks for reaching us. Your message has been sent!")
        return 'Success'

    except smtplib.SMTPException as e:
        flash('Something went wrong. Message not send.')
        print(e)
        return 'Failure'


def generate_ai_workout(duration, fitness_level, fitness_goal, equipment_access, running_type):
    """Generates an AI-based workout plan using the OpenAI API."""

    api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    f"Create a workout plan with only the workout name and details based on these criteria:\n"
                    f"- Workout Duration: '{duration} minutes'\n- Fitness Level: '{fitness_level}'\n- "
                    f"Fitness Goal: '{fitness_goal}'\n- Equipment Access: '{equipment_access}'\n- "
                    f"Running Type: '{running_type}'\n\n"
                    "Format:\n{\n  'workout_name': 'Name of the workout',\n  "
                    "'workout_details': [('Exercise Name', 'Description',"
                    " Sets, Repetitions, 'Rest Time in minutes'), ...]\n}\n"
                    "Note: Provide the response in this exact format, without any additional text.\n"
                    "Provide a workout name that reflects the workout's focus and goal, e.g., 'Intense Cardio Circuit' "
                    "or 'Beginners Full-Body Strength', with no punctuation marks.\n\n"
                    "For running workouts, if sets or rest times are not applicable, please default them to 1. "
                    "This means if a running exercise does not involve multiple sets or specific rest times, "
                    "you should still include '1' for sets and '1' for rest time in the workout details."
                )
            }
        ]

    )

    workout_output = completion.choices[0].message.content
    workout_output = workout_output.replace("'", '"')
    print(ast.literal_eval(workout_output))
    return ast.literal_eval(workout_output)


def get_number_of_workouts():
    """Return number of workouts."""
    return db.session.query(Workout).count() // 10 * 10


def get_number_of_exercises():
    """Return number of exercises."""
    return db.session.query(Exercises).count() // 10 * 10


def get_workout_from_db(workout_type, duration, fitness_level, fitness_goal=None, equipment_access=None,
                        running_type=None):
    """Return workout from the database based on user-provided criteria."""
    workouts = Workout.query.filter(
        Workout.workout_type == workout_type,
        Workout.workout_duration == duration,
        Workout.fitness_level == fitness_level,
        Workout.fitness_goal == fitness_goal,
        Workout.equipment_access == equipment_access,
        Workout.running_type == running_type
    ).all()

    print(workouts)
    print(workout_type, duration, fitness_level, fitness_goal, equipment_access, running_type)
    return workouts


def get_workout_id(workouts):
    """
    Return a random workout ID from the database in cass there are more than
    one workout that fits the user-provided criteria.
    """
    workout_ids = [workout.workout_id for workout in workouts]
    selected_workout_id = random.choice(workout_ids)
    return selected_workout_id


def get_workout_by_id(workout_id):
    """ Returns all the workout exercises from the database by a workout ID."""
    workout_details = db.session.query(
        Workout.workout_name,
        Exercises.exercise_name,
        Exercises.exercise_description,
        WorkoutExercises.sets,
        WorkoutExercises.repetitions,
        WorkoutExercises.rest_time
    ).join(WorkoutExercises, WorkoutExercises.exercise_id == Exercises.exercise_id) \
        .join(Workout, Workout.workout_id == WorkoutExercises.workout_id) \
        .filter(Workout.workout_id == workout_id) \
        .all()
    return workout_details
