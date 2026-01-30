from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.core.paginator import Paginator

from datetime import date


from tracker.forms import HabitForm, SignupForm, LoginForm
from tracker.models import Habit, Habit_log


# Create your views here.
@login_required
def dashboard(request):
    habits_list = Habit.objects.filter(user=request.user).order_by('id')
    if habits_list.exists():
        return redirect('user_dashboard_habits')

    return render(request, 'tracker/dashboard.html')

@login_required
def user_dashboard_habits(request):
    habits_list = Habit.objects.filter(user=request.user).order_by('id')
    paginator = Paginator(habits_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    today = date.today()
    logs = Habit_log.objects.filter(habit__in=page_obj, date=today)

    log_map = {log.habit.id: log for log in logs}

    return render(request, 'tracker/successful_added_habit_page.html', {
    'page_obj': page_obj,
    'logs': log_map,
    'today': today,
})


@login_required
def add_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect('user_dashboard_habits')
    else:
        form = HabitForm()

    return render(request, 'tracker/add_habit.html', {'form': form})

@login_required
def delete_habit(request, habit_id):
    if request.method == 'POST':
        habit = get_object_or_404(Habit, id=habit_id, user=request.user)
        habit.delete()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Habit deleted'})

        return redirect('tracker/user_dashboard_habits')

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@login_required
def mark_complete(request):
    if request.method == 'POST':
        habit_ids = request.POST.getlist('habit_ids')
        today = date.today()
        for habit in Habit.objects.filter(user=request.user):
            Habit_log.objects.update_or_create(
                habit=habit,
                date=today,
                defaults={'completed': str(habit.id) in habit_ids}
            )
    return redirect('tracker/user_dashboard_habits')


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def delete_account_view(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        return redirect('dashboard')
    return render(request, 'tracker/delete_account.html')
