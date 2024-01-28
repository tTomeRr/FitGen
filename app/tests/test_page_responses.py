import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config.update({'TESTING': True})

    with app.test_client() as client:
        yield client


def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200


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
