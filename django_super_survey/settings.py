from django import forms
from django.conf import settings
from django_super_survey import constants


def get_setting(name, default):
    return getattr(settings, f"SURVEY_{name}", default)


DEFAULT_FORM_FIELDS = {
    constants.TEXT: forms.CharField,
    constants.SELECT_MULTIPLE: forms.MultipleChoiceField,
}
FORM_FIELDS = get_setting('FORM_FIELDS', DEFAULT_FORM_FIELDS)


DEFAULT_STORAGE_CLASS = 'django.core.files.storage.FileSystemStorage'
STORAGE_CLASS = get_setting('STORAGE_CLASS', DEFAULT_STORAGE_CLASS)

DEFAULT_STORAGE_KWARGS = {
    'location': settings.MEDIA_ROOT,
    'base_url': settings.MEDIA_URL,
}
STORAGE_KWARGS = get_setting('STORAGE_KWARGS', DEFAULT_STORAGE_KWARGS)
