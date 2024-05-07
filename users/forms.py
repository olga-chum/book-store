from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from users.models import User

class UserLoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ['username', 'password']
   
    username = forms.CharField()
    password = forms.CharField()

class UserRegistrationForm(UserCreationForm):

    # confirmation = forms.BooleanField(widget=forms.RadioSelect(attrs={"class": "inputContainer__txt"}))
    # email= forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class":"inputContainer__txt"}))

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
            "phone"
        )
    def clean_confirmation(self):
        if self.cleaned_data["confirmation"] is not True:
            raise forms.ValidationError("You must confirm!")

    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()
    phone = forms.CharField()


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
    email = forms.CharField()