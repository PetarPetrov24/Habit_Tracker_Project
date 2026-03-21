import pytest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from tracker_app.forms import SignupForm

@pytest.mark.django_db
def test_false_login_user():
    User.objects.create_user(username='randomuser', password='notactualuser')

    user = authenticate(username='randomuser', password='wrongpass')

    assert user is None

@pytest.mark.django_db
def test_validating_two_passwords_while_user_register():
    form_data = {
        'username': 'testuser',
        'password1': 'StrongPassword123',
        'password2': 'StrongPassword123',
    }

    form = SignupForm(data=form_data)
    assert form.is_valid()

    form_data['password2'] = 'DifferentPassword123'
    form = SignupForm(data=form_data)
    assert not form.is_valid()
    assert 'password2' in form.errors
    assert any('match' in msg.lower() for msg in form.errors['password2'])