import re
from django import forms
from django.template.defaulttags import comment

# from distutils.command.clean import clean


class CreateOrderForm(forms.Form):

    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField(required=False)
    phone_number = forms.CharField()
    delivery_address = forms.CharField()
    flat = forms.CharField(required=False)
    comment = forms.CharField(required=False)
    # payment_on_get = forms.ChoiceField(choices=[('0', 'False'),
                                                # ('1', 'True'),],)

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        # Удалите все символы, кроме цифр, из номера телефона
        cleaned_phone_number = re.sub(r'\D', '', phone_number)
        pattern = re.compile(r'^\d{11}$')
        if not pattern.match(cleaned_phone_number):
            raise forms.ValidationError("Неверный формат номера телефона")

        return cleaned_phone_number