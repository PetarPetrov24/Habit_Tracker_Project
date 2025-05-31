from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10, default="✅", blank=True)
    category = models.CharField(max_length=20, choices=[
        ('health', 'Health'),
        ('work', 'Work'),
        ('personal', 'Personal'),
        ('finance', 'Finance'),
    ], default='personal')
    frequency = models.CharField(max_length=10, choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ], default='daily')
    target_per_day = models.IntegerField(default=1)
    difficulty = models.CharField(max_length=10, choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ], default='medium')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Habit_log(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.habit.name} - {self.date} - {'Done' if self.completed else 'Missed'}"

