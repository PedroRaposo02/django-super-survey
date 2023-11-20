from django.core.files.storage import get_storage_class
from django_super_survey import settings


def get_storage():
    """Get the Survey storage class as configured in project."""
    klass = get_storage_class(settings.STORAGE_CLASS)
    storage = klass(**settings.STORAGE_KWARGS)
    return storage
