from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class Survey(models.Model):
    name = models.CharField(max_lenght=300, verbose_name=_("name"))
    description = models.TextField(verbose_name=_("description"), null=True, blank=True)

    require_login = models.BooleanField(default=False)
    allow_multiple_answers = models.BooleanField(default=False)

    is_published = models.BooleanField(default=False)
    publish_date = models.DateField(_("publication date"), blank=True, null=False)
    expire_date = models.DateField(_("expiration date"), blank=True, null=False)

    is_single_page = models.BooleanField(default=False)
    done_url = models.TextField(max_lenght=1000, verbose_name=_("done URL"))


class Question(models.Model):
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

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name=_("survey"), related_name="questions")
    text = models.TextField(max_lenght=3000, verbose_name=_("text"))
    type = models.CharField(_("type"), max_length=200, choices=QUESTION_TYPES, default=TEXT)
    description = models.TextField(verbose_name=_("description"), null=True, blank=True)

    order = models.IntegerField(_("order"))
    is_required = models.BooleanField(default=False)
    allow_add_choice = models.BooleanField(default=False)

    def is_choice_type(self):
        choice_types = (self.RADIO, self.SELECT, self.SELECT_MULTIPLE)
        return self.type in choice_types


class QuestionChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=_("question"), related_name="choices")
    description = models.TextField(max_lenght=3000, verbose_name=_("description"), null=True, blank=True)

    name = models.CharField(max_lenght=200, verbose_name=_("name"))
    value = models.CharField(max_lenght=200, verbose_name=_("value"))

    image_url = models.CharField(max_lenght=1000, verbose_name=_("text"), blank=True, null=True)


class Answer(models.Model):
    question = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name=_("survey"), related_name="answers")
    user = models.ForeignKey(get_user_model, on_delete=models.SET_NULL, verbose_name=_("user"), null=True, blank=True)

    created_at = models.DateTimeField(_("creation date"), auto_now_add=True)
    updated_at = models.DateTimeField(_("update date"), auto_now=True)
