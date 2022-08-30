from django.db import models
from django.contrib.auth.models import User

class Business(models.Model):
    user = models.ForeignKey(User, blank=False, null=True)
    when = models.DateTimeField("date created", auto_now_add=True)
