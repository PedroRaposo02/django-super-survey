import json

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from django_super_survey import constants
from django_super_survey import querysets
from django_super_survey import storage


def make_survey_image_path(instance, filename):
    ext = filename.split('.')[-1]
    return f"survey/{instance.slug}.{ext}"


class Survey(models.Model):
    name = models.CharField(max_length=300, verbose_name=_("name"))
    slug = models.SlugField(max_length=300, verbose_name=_("slug"), blank=True)
    description = models.TextField(verbose_name=_("description"), null=True, blank=True)
    image = models.ImageField(
        upload_to=make_survey_image_path,
        storage=storage.get_storage(),
        null=True, blank=True,
    )

    vote_require_login = models.BooleanField(default=False)
    results_require_login = models.BooleanField(default=False)
    allow_multiple_answers = models.BooleanField(default=False)

    is_published = models.BooleanField(default=False)
    publish_date = models.DateField(_("publication date"), null=True, blank=True)
    expire_date = models.DateField(_("expiration date"), null=True, blank=True)

    is_single_page = models.BooleanField(default=False)
    done_url = models.TextField(max_length=1000, verbose_name=_("done URL"), null=True, blank=True)

    objects = querysets.SurveyQuerySet.as_manager()

    def __str__(self):
        return self.name

    def is_voted_by(self, user):
        voted = self.questions.filter(answers__user=user.id).exists()
        return voted


class Question(models.Model):
    QUESTION_TYPES = constants.QUESTION_TYPES

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name=_("survey"), related_name="questions")
    text = models.TextField(max_length=3000, verbose_name=_("text"))
    type = models.CharField(_("type"), max_length=200, choices=QUESTION_TYPES, default=constants.TEXT)
    description = models.TextField(verbose_name=_("description"), null=True, blank=True)

    order = models.IntegerField(_("order"))
    is_required = models.BooleanField(default=False)
    allow_add_choice = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    @property
    def is_choice_type(self):
        return self.type in constants.CHOICES_TYPE


class QuestionChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=_("question"), related_name="choices")
    description = models.TextField(max_length=3000, verbose_name=_("description"), null=True, blank=True)

    name = models.CharField(max_length=200, verbose_name=_("name"))
    value = models.CharField(max_length=200, verbose_name=_("value"))

    order = models.IntegerField(_("order"))
    image_url = models.CharField(max_length=1000, verbose_name=_("image URL"), null=True, blank=True)

    def __str__(self):
        return self.name


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=_("survey"), related_name="answers")
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, verbose_name=_("user"), null=True, blank=True, related_name="question_answers")

    value = models.CharField(max_length=200, verbose_name=_("value"))

    created_at = models.DateTimeField(_("creation date"), auto_now_add=True)
    updated_at = models.DateTimeField(_("update date"), auto_now=True)

    objects = querysets.AnswerQuerySet.as_manager()

    def __str__(self):
        return self.value

    @property
    def values(self):
        return json.loads(self.value)
