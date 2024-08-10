from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from users.models import User
import phonenumbers

class UserLoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ['username', 'password']
   
    username = forms.CharField()
    password = forms.CharField()

class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
            "phone_number"
        )

    def clean_confirmation(self):
        if self.cleaned_data["confirmation"] is not True:
            raise forms.ValidationError("You must confirm!")

    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()
    phone_number = forms.CharField()


class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "phone_number",
            'middle_name'
        )

    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    phone_number = forms.CharField()
    middle_name = forms.CharField(required=False)