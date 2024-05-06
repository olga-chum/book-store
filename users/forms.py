from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from users.models import User


class UserLoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ['email', 'password']
   
    email = forms.CharField()
    password = forms.CharField()

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField()
    password2 = forms.CharField()


class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
        )

    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()