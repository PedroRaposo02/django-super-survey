from django.utils.translation import gettext_lazy as _

TEXT = "text"
SHORT_TEXT = "short-text"
RADIO = "radio"
SELECT = "select"
SELECT_MULTIPLE = "select-multiple"
INTEGER = "integer"
FLOAT = "float"
DATE = "date"

QUESTION_TYPES = (
    (TEXT, _("text (multiple line)")),
    (SHORT_TEXT, _("short text (one line)")),
    (RADIO, _("radio")),
    (SELECT, _("select")),
    (SELECT_MULTIPLE, _("Select Multiple")),
    (INTEGER, _("integer")),
    (FLOAT, _("float")),
    (DATE, _("date")),
)

CHOICES_TYPE = (RADIO, SELECT, SELECT_MULTIPLE)
