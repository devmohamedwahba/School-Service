from django.db import models
import datetime
from dateutil.relativedelta import relativedelta
from django.core.validators import MaxValueValidator


class Student(models.Model):
    name = models.CharField(max_length=255)
    birth_date = models.DateField(default=datetime.date(2008, 1, 1))
    total = models.FloatField(validators=[MaxValueValidator(400)])

    @property
    def age_calculated(self):
        end_date = datetime.date(2020, 10, 1)
        start_date = self.birth_date

        diff = relativedelta(end_date, start_date)

        years = diff.years
        months = diff.months
        days = diff.days

        return f'{years} سنه | {months}  شهر | {days} يوم'

    @property
    def total_percentage(self):
        calc_total = (self.total / 400) * 100
        return f'{round(calc_total, 2)} %'

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-total']
