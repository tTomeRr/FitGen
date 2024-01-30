from dotenv import load_dotenv
import pytest
from app import create_app, db
import psycopg2
import os


@pytest.fixture
def app():
    load_dotenv(dotenv_path='.env.test', override=True)
    app = create_app()
    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_db_connection(app):
    try:
        with psycopg2.connect(
                dbname=os.getenv('POSTGRES_DB'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD')
        ) as conn:
            print('Connected to the PostgreSQL server.')
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        pytest.fail(f"Database connection failed: {error}")

def test_database_retrieval(client):
    sql_statement = """
        SELECT exercise_name, exercises.exercise_description, sets, repetitions, rest_time
        FROM workouts
        JOIN workoutexercises ON workouts.workout_id = workoutexercises.workout_id
        JOIN exercises ON workoutexercises.exercise_id = exercises.exercise_id
        WHERE workouts.workout_id = 4;
    """

    with client.application.app_context():
        with psycopg2.connect(
                dbname=os.getenv('POSTGRES_DB'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'),

        ) as conn:
            with conn.cursor() as cur:
                cur.execute(sql_statement)
                results = cur.fetchall()
                print(results)
                assert results


