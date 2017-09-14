from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    user = models.OneToOneField(User, related_name='person')

    def __str__(self):
        return "%s" % self.user.username
