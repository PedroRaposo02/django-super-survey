from django.db import models
from django.utils.timezone import now


class SurveyQuerySet(models.QuerySet):
    def annotate_is_voted_by(self, user):
        if user.is_anonymous:
            return self.annotate(
                voted=models.Value(False, output_field=models.BooleanField())
            )

        from django_super_survey.models import Question

        subquery = Question.objects\
            .filter(survey=models.OuterRef('id'), answers__user=user.id)\
            .values('id')[:1]
        qs = self.annotate(voted=models.Subquery(
            subquery,
            output_field=models.BooleanField()
        ))
        return qs

    def annotate_is_expired(self):
        return self.annotate(
            is_expired=models.ExpressionWrapper(
                models.Q(expire_date__lt=now()),
                output_field=models.BooleanField(),
            )
        )


class AnswerQuerySet(models.QuerySet):
    def group_by_values(self):
        return self.values('value')\
            .annotate(count=models.Count('value'))\
            .order_by('-count')

    def annotate_percentage(self):
        total = models.Value(self.count())
        return self\
            .group_by_values()\
            .annotate(percentage=models.ExpressionWrapper(
                models.F('count') * 100.0 / total,
                output_field=models.FloatField()
            ))
