import pytest
from app import create_app
from app.utils import send_mail


@pytest.fixture
def client():
    app = create_app()
    app.config.update({'TESTING': True})
    with app.test_client() as client:
        yield client


def test_send_email(client):

    name, email, phone, message = "test", "test@test.com", "1234", "test"

    with client.application.test_request_context():
        response = send_mail(name, email, phone, message)
        assert response == "Success"
