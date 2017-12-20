from django.db import models
from django.contrib.postgres.fields import JSONField

class LoveCalculation(models.Model):

    activity_id = models.IntegerField()
    results = JSONField()

    def __str__(self):
        return str(self.activity_id)
