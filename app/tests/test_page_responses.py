import pytest
from app import create_app
from dotenv import load_dotenv
import psycopg2
import os


@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_workout_page(client):
    response = client.get('/workout')
    assert response.status_code == 200


def test_run_page(client):
    response = client.get('/workout/run')
    assert response.status_code == 200


def test_strength_page(client):
    response = client.get('/workout/strength')
    assert response.status_code == 200


def test_ai_workout_page(client):
    response = client.get('/get_ai_workouts')
    assert response.status_code == 200
