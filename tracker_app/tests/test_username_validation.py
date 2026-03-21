import pytest
from tracker_app.forms import SignupForm

@pytest.mark.django_db
def test_username_below_six_characters_field():
    form_data = {
        'username': 'abc',
        'password1': 'Strongpass123',
        'password2': 'Strongpass123',
    }

    form = SignupForm(data=form_data)
    assert not form.is_valid()
    assert 'username' in form.errors
    assert any("at least 6 characters" in msg for msg in form.errors['username'])

@pytest.mark.django_db
def test_empty_username_error_field():
    form_data = {
        'username': '',
        'password1': 'Strongpass999',
        'password2': 'Strongpass999',
    }

    form = SignupForm(data=form_data)
    assert not form.is_valid()
    errors = form.errors.as_data()
    assert 'username' in errors
    assert any("Username cannot be empty." in str(e) for e in errors['username'])

@pytest.mark.django_db
def test_username_using_special_symbols_error():
    form_data = {
        'username': 'kaloyan@!#',
        'password1': 'Strongpass999',
        'password2': 'Strongpass999',
    }

    form = SignupForm(data=form_data)
    assert not form.is_valid()
    errors = form.errors.as_data()
    assert 'username' in errors
    assert any("Username can only contain letters, numbers, and underscores." in str(e) for e in errors['username'])
