from django import template
import phonenumbers

register = template.Library()

@register.filter
def phone_format(phone_number):
    parsed_number = phonenumbers.parse(phone_number, "RU")
    formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    return formatted_number