import pytest
from app import create_app, db


@pytest.fixture
def client():
    app = create_app()
    app.config.update({'TESTING': True})

    with app.test_client() as client:
        yield client


def test_database_connection(client):
    with client.application.app_context():
        with db.engine.begin() as conn:
            response = conn.exec_driver_sql("SELECT 1").all()
            assert response is not None


def test_database_retrieval(client):

    sql_statement = \
        """
            SELECT exercise_name, exercises.exercise_description, sets, repetitions, rest_time
            FROM workouts
            JOIN workoutexercises ON workouts.workout_id = workoutexercises.workout_id
            JOIN exercises ON workoutexercises.exercise_id = exercises.exercise_id
            WHERE workouts.workout_id = 4;
        """

    with client.application.app_context():
        with db.engine.begin() as conn:
            response = conn.exec_driver_sql(sql_statement).all()
            print(response)
            assert response
