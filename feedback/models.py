from django.db import models

class GoalFeedback(models.Model):

    feedback = models.BooleanField(default=True)
