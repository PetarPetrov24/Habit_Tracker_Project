from django.contrib.auth.models import User
import pytest
from django.test import Client

@pytest.mark.django_db
def test_home_view(client):
    client = Client()

    user = User.objects.create_user(username='testuser', password='password123')
    client.login(username='testuser', password='password123')

    response = client.get("/")
    assert response.status_code == 200