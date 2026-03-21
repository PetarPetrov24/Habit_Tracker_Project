import pytest
from tracker_app.models import Habit, Habit_log
from django.contrib.auth.models import User
from datetime import date

@pytest.mark.django_db
def test_habit_creation():
    user = User.objects.create(username="tester")
    habit = Habit.objects.create(user=user, name="Test Habit")
    assert habit.name == "Test Habit"
    assert habit.user.username == "tester"

@pytest.mark.django_db
def test_habit_log_creation():
    user = User.objects.create(username="tester2")
    habit = Habit.objects.create(user=user, name="Test Habit 2")
    habit_log = Habit_log.objects.create(habit=habit, date=date.today())
    assert habit_log.habit.name == "Test Habit 2"
    assert habit_log.completed is False

@pytest.mark.django_db
def test_habit_log_complete_option():
    user = User.objects.create(username="tester2")
    habit = Habit.objects.create(user=user, name="Running")

    log1 = Habit_log.objects.create(habit=habit, date=date.today())
    assert log1.completed is False
    assert str(log1) == f"Running - {log1.date} - Missed"

    log2 = Habit_log.objects.create(habit=habit, date=date.today(), completed=True)
    assert log2.completed is True
    assert str(log2) == f"Running - {log2.date} - Done"


