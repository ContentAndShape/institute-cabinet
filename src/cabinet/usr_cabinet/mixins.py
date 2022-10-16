from django.db import models
from django.contrib.auth.models import User


class UserReprMixin(User):

    class Meta:
        abstract = True
        ordering = ['last_name']

    def __str__(self) -> str:
        return self.get_full_name()


class NameMixin(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self) -> str:
        return self.name