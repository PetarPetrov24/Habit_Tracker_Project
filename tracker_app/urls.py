from django.urls import path
from django.urls.conf import include

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('user-habits/', views.user_dashboard_habits, name='user_dashboard_habits'),
    path('add/', views.add_habit, name='add_habit'),
    path('delete/<int:habit_id>/', views.delete_habit, name='delete_habit'),
    path('mark/', views.mark_complete, name='mark_complete'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('delete-account/', views.delete_account_view, name='delete_account'),
]