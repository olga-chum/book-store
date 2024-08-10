from django import forms

class ContactForm(forms.Form):
    first_name = forms.CharField(min_length=2, widget=forms.TextInput(attrs={'placeholder': 'Введите ваше имя', 'class': 'about__question_txt'}))
    username = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Введите вашу почту', 'class': 'about__question_txt'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Чем мы можем вам помочь?', 'class': 'about__question_txt', 'style':"height: 3rem; padding-top: 0.4rem;"}))
