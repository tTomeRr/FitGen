"""
This module defines the database tables for the flex application, and the association between them.
"""

from . import db

class Workout(db.Model):
    """Represents a workout, with details about its type, duration, fitness level, etc."""
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
    """Represents an exercise, with details about its type and description."""
    __tablename__ = 'exercises'
    exercise_id = db.Column(db.Integer, primary_key=True)
    exercise_name = db.Column(db.String)
    exercise_type = db.Column(db.String)
    exercise_description = db.Column(db.String)


class WorkoutExercises(db.Model):
    """Represents the exercises each workout will have and
    includes details about sets, repetitions, and rest time."""
    __tablename__ = 'workoutexercises'
    workout_id = db.Column(db.Integer, db.ForeignKey('Workouts.workout_id'), primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('Exercises.exercise_id'), primary_key=True)
    sets = db.Column(db.Integer)
    repetitions = db.Column(db.String(20))
    rest_time = db.Column(db.String(20))
