from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

from .validation import validate_username, validate_password, validate_passwords_match

from .models import Habit

ICON_CHOICES = [
    ("🏃", "🏃 Health"),
    ("💼", "💼 Work"),
    ("📖", "📖 Personal"),
    ("📈", "📈 Finance"),
]


class HabitForm(forms.ModelForm):
    icon = forms.ChoiceField(choices=ICON_CHOICES, label="Choose an Icon")

    class Meta:
        model = Habit
        fields = ['name', 'category', 'icon', 'frequency', 'target_per_day', 'difficulty']


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        validate_username(username)
        return username

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        pass1 = cleaned_data.get('password1')
        pass2 = cleaned_data.get('password2')
        try:
            validate_passwords_match(pass1, pass2)
        except ValidationError as e:
            self.add_error('password2', e)
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password1"]
        user.set_password(password)
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError(
                    "Please enter a correct username and password. Note that both fields may be case-sensitive."
                )
            self.user = user
        return cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)