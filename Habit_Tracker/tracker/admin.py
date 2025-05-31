from django.contrib import admin

from tracker.models import Habit, Habit_log

# Register your models here.
admin.site.register(Habit)
admin.site.register(Habit_log)