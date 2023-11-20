from django import forms
from django_super_survey import settings


def get_form_field(type_):
    return settings.FORM_FIELDS.get(type_, forms.CharField)
